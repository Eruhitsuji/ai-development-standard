#!/usr/bin/env python3
"""Analyze an AI development history archive and emit runtime findings."""

import argparse
import fnmatch
import hashlib
import json
from collections import defaultdict
from pathlib import Path


WRITE_EVENT_KINDS = {"file_create", "file_edit", "file_delete", "patch"}
PROTECTED_COMMAND_MARKERS = [
    "git reset --hard",
    "git push --force",
    "gh release",
    " deploy",
    " release",
    " rollback",
]


def sha256_text(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8", errors="replace")).hexdigest()


def read_jsonl(path: Path):
    records = []
    with path.open("r", encoding="utf-8") as stream:
        for line_number, line in enumerate(stream, start=1):
            stripped = line.strip()
            if not stripped:
                continue
            try:
                records.append(json.loads(stripped))
            except json.JSONDecodeError as exc:
                raise SystemExit(f"{path}:{line_number}: invalid JSONL: {exc}") from exc
    return records


def json_objects_from_text(text: str):
    try:
        yield json.loads(text)
        return
    except json.JSONDecodeError:
        pass

    for line in text.splitlines():
        stripped = line.strip()
        if not stripped or not stripped.startswith(("{", "[")):
            continue
        try:
            yield json.loads(stripped)
        except json.JSONDecodeError:
            continue


def first_string(obj: dict, keys):
    for key in keys:
        value = obj.get(key)
        if isinstance(value, str) and value:
            return value
    return None


def first_int(obj: dict, keys):
    for key in keys:
        value = obj.get(key)
        if isinstance(value, int):
            return value
        if isinstance(value, str) and value.lstrip("-").isdigit():
            return int(value)
    return None


def infer_event(obj: dict, provider: str, source_id: str):
    if not isinstance(obj, dict):
        return None

    if obj.get("record_type") == "event" and isinstance(obj.get("event"), dict):
        event = dict(obj)
        event.setdefault("provider", provider)
        event.setdefault("source", {"source_id": source_id})
        event.setdefault("session_id", source_id)
        event.setdefault("event_id", event_id(event))
        return event

    native_type = first_string(obj, ["type", "kind", "event_type", "eventType"])
    role = first_string(obj, ["role", "speaker"])
    command = first_string(obj, ["command", "cmd", "shell_command", "shellCommand"])
    exit_code = first_int(obj, ["exit_code", "exitCode", "returncode", "status"])
    path = first_string(obj, ["path", "file_path", "filePath", "target_path", "targetPath"])
    message = first_string(obj, ["message", "content", "text", "output", "stderr", "stdout"])
    tool = first_string(obj, ["tool", "tool_name", "toolName", "name"])

    kind = None
    event_payload = {}

    if command:
        command_text = command.strip()
        kind = "git_command" if command_text.startswith("git ") else "command_start"
        if exit_code is not None:
            kind = "command_result"
        event_payload.update({"command": command, "exit_code": exit_code})
    elif path and native_type:
        lowered = native_type.casefold()
        if "delete" in lowered:
            kind = "file_delete"
        elif "create" in lowered or "write" in lowered:
            kind = "file_create"
        elif "edit" in lowered or "patch" in lowered or "update" in lowered:
            kind = "file_edit"
        elif "read" in lowered:
            kind = "file_read"
        event_payload["path"] = path
    elif role in {"user", "human"}:
        kind = "user_message"
        event_payload["message"] = message
    elif role == "assistant":
        kind = "assistant_message"
        event_payload["message"] = message
    elif tool:
        kind = "tool_call"
        event_payload["tool"] = tool
    elif native_type and "approval" in native_type.casefold():
        kind = "approval_result" if "result" in native_type.casefold() else "approval_request"
        event_payload["message"] = message

    if not kind:
        return None

    session_id = first_string(
        obj,
        ["session_id", "sessionId", "conversation_id", "conversationId", "thread_id", "threadId"],
    ) or source_id
    event = {
        "record_type": "event",
        "provider": first_string(obj, ["provider"]) or provider,
        "session_id": session_id,
        "timestamp": first_string(obj, ["timestamp", "created_at", "createdAt", "time"]),
        "cwd": first_string(obj, ["cwd", "project_path", "projectPath", "workingDirectory"]),
        "event": {"kind": kind, **event_payload},
        "source": {
            "source_id": source_id,
            "provider_native_type": native_type,
        },
    }
    event["event_id"] = event_id(event)
    return event


def event_id(event: dict) -> str:
    payload = json.dumps(event, ensure_ascii=False, sort_keys=True)
    return "sha256:" + sha256_text(payload)


def extract_events(records):
    events = []
    for record in records:
        if record.get("record_type") == "event":
            normalized = infer_event(record, record.get("provider", "unknown"), record.get("source_id", "event"))
            if normalized:
                events.append(normalized)
        elif record.get("record_type") == "raw_source":
            provider = record.get("provider", "unknown")
            source_id = record.get("source_id", "raw_source")
            for obj in json_objects_from_text(record.get("content", "")):
                normalized = infer_event(obj, provider, source_id)
                if normalized:
                    events.append(normalized)
    return events


def normalize_path(path: str) -> str:
    return path.replace("\\", "/").lstrip("./")


def matches_any_scope(path: str, scopes) -> bool:
    if not scopes:
        return True
    normalized = normalize_path(path)
    for scope in scopes:
        pattern = normalize_path(scope)
        if fnmatch.fnmatch(normalized, pattern):
            return True
        if pattern.endswith("/**") and normalized.startswith(pattern[:-3]):
            return True
    return False


def make_finding(
    category: str,
    subtype: str,
    severity: str,
    confidence: float,
    rule_ids,
    evidence_events,
    summary: str,
    expected: str,
    observed: str,
    impact: str,
    suggested_change: str,
    standard_version,
    standard_commit,
):
    sessions = sorted({event.get("session_id", "") for event in evidence_events if event.get("session_id")})
    evidence = [
        {
            "event_id": event.get("event_id"),
            "session_id": event.get("session_id"),
            "provider": event.get("provider"),
            "kind": event.get("event", {}).get("kind"),
            "source_id": event.get("source", {}).get("source_id"),
        }
        for event in evidence_events[:10]
    ]
    fingerprint_payload = json.dumps(
        {
            "category": category,
            "subtype": subtype,
            "rule_ids": rule_ids,
            "summary": summary,
            "expected": expected,
            "observed": observed,
        },
        ensure_ascii=False,
        sort_keys=True,
    )
    return {
        "finding_id": "sha256:" + sha256_text(fingerprint_payload),
        "category": category,
        "subtype": subtype,
        "severity": severity,
        "confidence": confidence,
        "standard": {
            "version": standard_version,
            "commit": standard_commit,
            "rule_ids": rule_ids,
        },
        "sessions": sessions,
        "evidence": evidence,
        "analysis": {
            "summary": summary,
            "expected": expected,
            "observed": observed,
            "impact": impact,
            "suggested_change": suggested_change,
        },
        "human_review": "not_reviewed",
    }


def detect_weak_project_association(records, standard_version, standard_commit):
    findings = []
    for record in records:
        if record.get("record_type") != "source_file":
            continue
        association = record.get("project_association", {})
        if association.get("method") != "text_fallback":
            continue
        pseudo_event = {
            "event_id": record.get("source_id"),
            "session_id": record.get("source_id"),
            "provider": record.get("provider"),
            "event": {"kind": "warning"},
            "source": {"source_id": record.get("source_id")},
        }
        findings.append(
            make_finding(
                "tool_compatibility",
                "weak_project_association",
                "low",
                0.75,
                ["RUNTIME_EVIDENCE.md", "RUNTIME-COLLECT-001"],
                [pseudo_event],
                "Project association used full-text fallback instead of provider metadata.",
                "Runtime collection should associate sessions through provider-owned project metadata where possible.",
                "At least one source matched only through fallback text search.",
                "The archive may include unrelated provider history if the fallback match is too broad.",
                "Prefer exact metadata matching or inspect the provider schema before using this evidence.",
                standard_version,
                standard_commit,
            )
        )
    return findings


def detect_write_scope_violations(events, scopes, standard_version, standard_commit):
    if not scopes:
        return []
    offenders = []
    for event in events:
        payload = event.get("event", {})
        if payload.get("kind") not in WRITE_EVENT_KINDS:
            continue
        paths = list(payload.get("paths") or [])
        if payload.get("path"):
            paths.append(payload["path"])
        outside = [path for path in paths if not matches_any_scope(path, scopes)]
        if outside:
            annotated = dict(event)
            annotated["event"] = {**payload, "outside_write_scope": outside}
            offenders.append(annotated)
    if not offenders:
        return []
    return [
        make_finding(
            "project_violation",
            "write_scope_violation",
            "medium",
            0.95,
            ["TASK_MANAGEMENT.md", "MULTI_AGENT_DEVELOPMENT.md"],
            offenders,
            "Runtime evidence includes file changes outside the declared write scope.",
            "Implementation should change only paths allowed by the task contract.",
            "One or more write events targeted paths outside the provided scope patterns.",
            "Parallel work may conflict or include unreviewed scope expansion.",
            "Review the task contract, split unrelated work, or update scope through an explicit human-approved issue change.",
            standard_version,
            standard_commit,
        )
    ]


def detect_repeated_command_failures(events, standard_version, standard_commit):
    failures = defaultdict(list)
    for event in events:
        payload = event.get("event", {})
        if payload.get("kind") != "command_result":
            continue
        exit_code = payload.get("exit_code")
        command = payload.get("command")
        if command and isinstance(exit_code, int) and exit_code != 0:
            failures[command].append(event)
    findings = []
    for command, command_events in failures.items():
        if len(command_events) < 2:
            continue
        findings.append(
            make_finding(
                "project_violation",
                "repeated_command_failure",
                "medium",
                0.9,
                ["TESTING.md", "DEFINITION_OF_DONE.md"],
                command_events,
                "The same command failed repeatedly during the session.",
                "Repeated failures should trigger diagnosis, a changed approach, or a blocker report.",
                f"The command failed {len(command_events)} times: {command}",
                "The executor may be retrying without resolving the underlying problem.",
                "Inspect the first failure, document the blocker if needed, and avoid reporting completion until verification passes.",
                standard_version,
                standard_commit,
            )
        )
    return findings


def detect_protected_operation_without_approval(events, standard_version, standard_commit):
    approval_seen = False
    offenders = []
    for event in events:
        payload = event.get("event", {})
        kind = payload.get("kind")
        if kind == "approval_result":
            approval_seen = True
            continue
        command = str(payload.get("command") or "").casefold()
        if command and any(marker in f" {command}" for marker in PROTECTED_COMMAND_MARKERS):
            if not approval_seen:
                offenders.append(event)
    if not offenders:
        return []
    return [
        make_finding(
            "project_violation",
            "protected_operation_without_approval",
            "high",
            0.85,
            ["AI_HUMAN_INTERACTION.md", "AI_PERMISSIONS.md"],
            offenders,
            "A protected operation appears before a recorded approval event.",
            "Destructive, release, deployment, rollback, and similar operations require explicit human approval.",
            "Runtime evidence shows a protected command before an approval result was observed.",
            "Human-only authority may have been bypassed or the evidence archive may be incomplete.",
            "Confirm whether approval occurred outside the captured history and update the task evidence or approval workflow.",
            standard_version,
            standard_commit,
        )
    ]


def detect_unrecognized_schema(records, events, standard_version, standard_commit):
    has_sources = any(record.get("record_type") == "source_file" for record in records)
    has_raw = any(record.get("record_type") == "raw_source" for record in records)
    if not has_sources or events or not has_raw:
        return []
    return [
        make_finding(
            "tool_compatibility",
            "provider_schema_unrecognized",
            "low",
            0.65,
            ["AI_TOOL_COMPATIBILITY.md", "RUNTIME_EVIDENCE.md"],
            [],
            "The archive contains raw provider evidence, but no normalized events were recognized.",
            "Provider evidence should normalize into common event records for deterministic checks.",
            "The analyzer could not infer supported event kinds from the captured provider data.",
            "Runtime evaluation coverage may be incomplete for this provider or provider version.",
            "Add a provider normalizer or fixture for this schema before relying on automated findings.",
            standard_version,
            standard_commit,
        )
    ]


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("archive")
    parser.add_argument("--output", default="ai-history-findings.jsonl")
    parser.add_argument("--events-output")
    parser.add_argument("--write-scope", action="append", default=[])
    parser.add_argument("--standard-version")
    parser.add_argument("--standard-commit")
    args = parser.parse_args()

    records = read_jsonl(Path(args.archive))
    events = extract_events(records)
    findings = []
    findings.extend(detect_weak_project_association(records, args.standard_version, args.standard_commit))
    findings.extend(detect_write_scope_violations(events, args.write_scope, args.standard_version, args.standard_commit))
    findings.extend(detect_repeated_command_failures(events, args.standard_version, args.standard_commit))
    findings.extend(detect_protected_operation_without_approval(events, args.standard_version, args.standard_commit))
    findings.extend(detect_unrecognized_schema(records, events, args.standard_version, args.standard_commit))

    if args.events_output:
        events_output = Path(args.events_output)
        events_output.parent.mkdir(parents=True, exist_ok=True)
        with events_output.open("w", encoding="utf-8", newline="\n") as stream:
            for event in events:
                stream.write(json.dumps(event, ensure_ascii=False, sort_keys=True))
                stream.write("\n")

    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    with output.open("w", encoding="utf-8", newline="\n") as stream:
        for finding in findings:
            stream.write(json.dumps(finding, ensure_ascii=False, sort_keys=True))
            stream.write("\n")

    print(f"Extracted {len(events)} normalized events.")
    print(f"Wrote {len(findings)} findings to {output}.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
