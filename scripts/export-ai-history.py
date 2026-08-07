#!/usr/bin/env python3
"""Export local AI development history for a target project.

The collector is intentionally conservative:

- it reads provider-owned local persistence directories;
- it associates sessions with a project through metadata keys first;
- it omits raw content unless --include-raw is provided;
- it never uploads or reports findings to GitHub.
"""

import argparse
import datetime as dt
import hashlib
import json
import os
from pathlib import Path


SUPPORTED_PROVIDERS = ("claude-code", "codex")
METADATA_KEYS = {
    "cwd",
    "currentWorkingDirectory",
    "project_path",
    "projectPath",
    "repoPath",
    "repositoryPath",
    "rootPath",
    "workspace",
    "workspaceFolder",
    "workspaceFolders",
    "workingDirectory",
}
TEXT_SUFFIXES = {".json", ".jsonl", ".ndjson", ".log", ".txt", ".md"}


def utc_now() -> str:
    return dt.datetime.now(dt.timezone.utc).isoformat()


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def stable_id(*parts: str) -> str:
    joined = "\0".join(parts).encode("utf-8", errors="replace")
    return "sha256:" + sha256_bytes(joined)


def safe_resolve(path: Path) -> Path:
    return path.expanduser().resolve()


def normalized_path_text(value: str) -> str:
    return value.replace("\\", "/").rstrip("/").casefold()


def path_matches_project(value, project_dir: Path, exact_root: bool) -> bool:
    if not isinstance(value, str) or not value.strip():
        return False

    candidate_text = os.path.expandvars(value.strip())
    project_text = normalized_path_text(str(project_dir))

    try:
        candidate = Path(candidate_text).expanduser()
        if candidate.is_absolute():
            resolved = safe_resolve(candidate)
            resolved_text = normalized_path_text(str(resolved))
            if exact_root:
                return resolved_text == project_text
            return resolved_text == project_text or resolved_text.startswith(project_text + "/")
    except (OSError, RuntimeError):
        pass

    candidate_norm = normalized_path_text(candidate_text)
    if exact_root:
        return candidate_norm == project_text
    return candidate_norm == project_text or candidate_norm.startswith(project_text + "/")


def provider_roots(provider: str, explicit_roots):
    roots = list(explicit_roots.get(provider, []))
    if roots:
        return unique_resolved_paths(roots)

    home = Path.home()
    appdata = os.environ.get("APPDATA")
    localappdata = os.environ.get("LOCALAPPDATA")

    if provider == "claude-code":
        roots.extend([home / ".claude", home / ".config" / "Claude"])
        if appdata:
            roots.append(Path(appdata) / "Claude")
        if localappdata:
            roots.append(Path(localappdata) / "Claude")
    elif provider == "codex":
        roots.extend([home / ".codex", home / ".config" / "codex"])
        if appdata:
            roots.append(Path(appdata) / "Codex")
        if localappdata:
            roots.append(Path(localappdata) / "Codex")

    return unique_resolved_paths(roots)


def unique_resolved_paths(paths):
    unique = []
    seen = set()
    for root in paths:
        try:
            resolved = safe_resolve(root)
        except (OSError, RuntimeError):
            continue
        key = str(resolved).casefold()
        if key not in seen:
            seen.add(key)
            unique.append(resolved)
    return unique


def parse_provider_root(value: str):
    if "=" not in value:
        raise argparse.ArgumentTypeError("provider root must use PROVIDER=PATH")
    provider, raw_path = value.split("=", 1)
    provider = provider.strip()
    if provider not in SUPPORTED_PROVIDERS:
        raise argparse.ArgumentTypeError(f"unsupported provider: {provider}")
    return provider, Path(raw_path.strip())


def candidate_files(root: Path, max_file_bytes: int):
    if not root.exists():
        return
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [
            name
            for name in dirnames
            if name not in {"node_modules", ".git", "__pycache__"}
        ]
        for filename in filenames:
            path = Path(dirpath) / filename
            if path.suffix.lower() not in TEXT_SUFFIXES:
                continue
            try:
                stat = path.stat()
            except OSError:
                continue
            if stat.st_size > max_file_bytes:
                continue
            yield path


def read_text(path: Path):
    data = path.read_bytes()
    return data.decode("utf-8", errors="replace"), data


def json_objects_from_text(text: str, suffix: str):
    suffix = suffix.lower()
    if suffix == ".json":
        try:
            yield json.loads(text)
        except json.JSONDecodeError:
            return
        return

    for line in text.splitlines():
        stripped = line.strip()
        if not stripped or not stripped.startswith(("{", "[")):
            continue
        try:
            yield json.loads(stripped)
        except json.JSONDecodeError:
            continue


def metadata_values(obj):
    values = []
    if isinstance(obj, dict):
        for key, value in obj.items():
            if key in METADATA_KEYS:
                values.extend(flatten_strings(value))
            values.extend(metadata_values(value))
    elif isinstance(obj, list):
        for item in obj:
            values.extend(metadata_values(item))
    return values


def flatten_strings(value):
    if isinstance(value, str):
        return [value]
    if isinstance(value, list):
        results = []
        for item in value:
            results.extend(flatten_strings(item))
        return results
    if isinstance(value, dict):
        return metadata_values(value)
    return []


def source_association(text: str, suffix: str, project_dir: Path, exact_root: bool, allow_text_fallback: bool):
    matches = []
    for obj in json_objects_from_text(text, suffix):
        for value in metadata_values(obj):
            if path_matches_project(value, project_dir, exact_root):
                matches.append(value)

    if matches:
        return {
            "matched": True,
            "method": "metadata",
            "matched_values": sorted(set(matches)),
        }

    if allow_text_fallback:
        project_text = normalized_path_text(str(project_dir))
        if project_text in normalized_path_text(text):
            return {
                "matched": True,
                "method": "text_fallback",
                "matched_values": [],
            }

    return {"matched": False, "method": "none", "matched_values": []}


def selected_providers(raw_values):
    values = raw_values or ["all"]
    if "all" in values:
        return list(SUPPORTED_PROVIDERS)
    ordered = []
    for value in values:
        if value not in ordered:
            ordered.append(value)
    return ordered


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--project-dir", default=".")
    parser.add_argument("--output", default="ai-development-history.jsonl")
    parser.add_argument("--provider", action="append", choices=["all", *SUPPORTED_PROVIDERS])
    parser.add_argument("--provider-root", action="append", type=parse_provider_root, default=[])
    parser.add_argument("--exact-root", action="store_true")
    parser.add_argument("--allow-text-fallback", action="store_true")
    parser.add_argument("--include-raw", action="store_true")
    parser.add_argument("--max-file-bytes", type=int, default=1_048_576)
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    project_dir = safe_resolve(Path(args.project_dir))
    explicit_roots = {provider: [] for provider in SUPPORTED_PROVIDERS}
    for provider, root in args.provider_root:
        explicit_roots[provider].append(root)

    providers = selected_providers(args.provider)
    records = [
        {
            "record_type": "archive_metadata",
            "schema_version": 1,
            "created_at": utc_now(),
            "project_dir": str(project_dir),
            "exact_root": args.exact_root,
            "include_raw": args.include_raw,
            "allow_text_fallback": args.allow_text_fallback,
            "providers": providers,
        }
    ]

    matched_count = 0
    for provider in providers:
        for root in provider_roots(provider, explicit_roots):
            for path in candidate_files(root, args.max_file_bytes):
                try:
                    text, data = read_text(path)
                except OSError:
                    continue
                association = source_association(
                    text,
                    path.suffix,
                    project_dir,
                    args.exact_root,
                    args.allow_text_fallback,
                )
                if not association["matched"]:
                    continue
                digest = sha256_bytes(data)
                source_id = stable_id(provider, str(path), digest)
                matched_count += 1
                records.append(
                    {
                        "record_type": "source_file",
                        "provider": provider,
                        "source_id": source_id,
                        "source_path": str(path),
                        "size_bytes": len(data),
                        "sha256": "sha256:" + digest,
                        "project_association": association,
                    }
                )
                if args.include_raw:
                    records.append(
                        {
                            "record_type": "raw_source",
                            "provider": provider,
                            "source_id": source_id,
                            "content": text,
                        }
                    )

    if args.dry_run:
        print(f"Matched {matched_count} provider source files for {project_dir}")
        return 0

    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    with output.open("w", encoding="utf-8", newline="\n") as stream:
        for record in records:
            stream.write(json.dumps(record, ensure_ascii=False, sort_keys=True))
            stream.write("\n")

    print(f"Wrote {len(records)} archive records to {output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
