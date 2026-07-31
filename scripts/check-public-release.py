#!/usr/bin/env python3
"""Run lightweight public-release readiness checks.

This script validates required public documentation and scans current tracked
text files for a small set of high-confidence secret patterns. It does not scan
Git history, Issues, pull requests, workflow logs, artifacts, forks, or caches.
Follow docs/PUBLIC_RELEASE_CHECKLIST.md before publication.
"""

from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]

REQUIRED_FILES = [
    "LICENSE",
    "SECURITY.md",
    "docs/QUICKSTART.md",
    "docs/QUICKSTART.ja.md",
    "docs/PROJECT_STATUS.md",
    "docs/PUBLIC_RELEASE_CHECKLIST.md",
]

SECRET_PATTERNS = {
    "private key": re.compile(
        r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----"
    ),
    "GitHub token": re.compile(r"\bgh[pousr]_[A-Za-z0-9]{30,255}\b"),
    "AWS access key": re.compile(r"\bAKIA[0-9A-Z]{16}\b"),
    "Slack token": re.compile(r"\bxox[baprs]-[A-Za-z0-9-]{10,}\b"),
    "OpenAI API key": re.compile(r"\bsk-[A-Za-z0-9]{20,}\b"),
}

MAX_FILE_SIZE = 2 * 1024 * 1024


def read_text(relative: str) -> str:
    return (ROOT / relative).read_text(encoding="utf-8")


def tracked_files() -> list[Path]:
    try:
        result = subprocess.run(
            ["git", "ls-files", "-z"],
            cwd=ROOT,
            check=True,
            capture_output=True,
        )
    except (FileNotFoundError, subprocess.CalledProcessError):
        return [
            path
            for path in ROOT.rglob("*")
            if path.is_file() and ".git" not in path.parts
        ]

    return [
        ROOT / item.decode("utf-8")
        for item in result.stdout.split(b"\0")
        if item
    ]


def check_required_files(errors: list[str]) -> None:
    for relative in REQUIRED_FILES:
        path = ROOT / relative
        if not path.is_file():
            errors.append(f"Missing public-release file: {relative}")
        elif path.stat().st_size == 0:
            errors.append(f"Public-release file is empty: {relative}")


def check_license(errors: list[str]) -> None:
    path = ROOT / "LICENSE"
    if not path.is_file():
        return
    text = path.read_text(encoding="utf-8")
    for marker in [
        "MIT License",
        "Copyright (c) 2026 Eruhitsuji",
        'THE SOFTWARE IS PROVIDED "AS IS"',
    ]:
        if marker not in text:
            errors.append(f"LICENSE missing expected MIT marker: {marker}")


def check_public_docs(errors: list[str]) -> None:
    checks = {
        "SECURITY.md": ["Reporting a Vulnerability", "Supported Versions"],
        "docs/QUICKSTART.md": [
            "python scripts/validate-standard.py",
            "python scripts/run-standard-evals.py",
            "python scripts/check-public-release.py",
        ],
        "docs/QUICKSTART.ja.md": ["英語版を優先", "check-public-release.py"],
        "docs/PROJECT_STATUS.md": ["Experimental Preview", "Known Limitations"],
        "docs/PUBLIC_RELEASE_CHECKLIST.md": [
            "Sensitive Information Review",
            "Post-Release Verification",
        ],
    }

    for relative, markers in checks.items():
        path = ROOT / relative
        if not path.is_file():
            continue
        text = path.read_text(encoding="utf-8")
        for marker in markers:
            if marker not in text:
                errors.append(f"{relative} missing required marker: {marker}")


def check_secrets(errors: list[str]) -> None:
    for path in tracked_files():
        if not path.is_file() or path.stat().st_size > MAX_FILE_SIZE:
            continue
        try:
            data = path.read_bytes()
        except OSError as exc:
            errors.append(f"Could not read {path.relative_to(ROOT)}: {exc}")
            continue
        if b"\0" in data:
            continue
        try:
            text = data.decode("utf-8")
        except UnicodeDecodeError:
            continue

        relative = path.relative_to(ROOT)
        for label, pattern in SECRET_PATTERNS.items():
            match = pattern.search(text)
            if match:
                line = text.count("\n", 0, match.start()) + 1
                errors.append(
                    f"Possible {label} in {relative}:{line}; remove or rotate it"
                )


def main() -> int:
    errors: list[str] = []
    check_required_files(errors)
    check_license(errors)
    check_public_docs(errors)
    check_secrets(errors)

    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        return 1

    print("Public release readiness checks passed for current tracked files.")
    print(
        "NOTE: Git history, Issues, pull requests, logs, artifacts, forks, and "
        "caches still require the manual release checklist."
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
