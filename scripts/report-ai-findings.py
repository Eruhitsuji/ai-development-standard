#!/usr/bin/env python3
"""Render sanitized runtime finding reports.

This script does not create GitHub Issues. It produces Markdown that a human or
reviewed automation can use after deduplication and privacy review.
"""

import argparse
import json
import os
import re
from pathlib import Path


SECRET_PATTERN = re.compile(
    r"(?i)\b(token|secret|api[_-]?key|password|credential)\b\s*[:=]\s*[^\s,;]{8,}"
)
PRIVATE_URL_PATTERN = re.compile(r"https?://[^\s)]+")


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


def redact(value: str) -> str:
    value = SECRET_PATTERN.sub(lambda match: f"{match.group(1)}=[REDACTED]", value)
    value = PRIVATE_URL_PATTERN.sub("[REDACTED_URL]", value)
    home = str(Path.home())
    if home and home in value:
        value = value.replace(home, "[REDACTED_HOME]")
    userprofile = os.environ.get("USERPROFILE")
    if userprofile and userprofile in value:
        value = value.replace(userprofile, "[REDACTED_HOME]")
    return value


def text(value) -> str:
    if value is None:
        return ""
    if isinstance(value, str):
        return redact(value)
    return redact(json.dumps(value, ensure_ascii=False, sort_keys=True))


def target_for_finding(finding: dict, requested_target: str) -> str:
    if requested_target != "auto":
        return requested_target
    category = finding.get("category")
    if category in {"standard_defect", "tool_compatibility", "unclear_guidance", "missing_rule", "conflicting_rules", "workflow_friction", "excessive_context", "efficiency_problem"}:
        return "upstream-standard"
    return "downstream-project"


def render_finding(finding: dict, requested_target: str, max_evidence_events: int) -> str:
    finding_id = finding.get("finding_id", "unknown")
    analysis = finding.get("analysis", {})
    standard = finding.get("standard", {})
    target = target_for_finding(finding, requested_target)
    evidence = finding.get("evidence", [])[:max_evidence_events]

    lines = [
        "# Runtime AI Finding",
        "",
        f"ADS-FINDING: {text(finding_id)}",
        "",
        "## Classification",
        "",
        f"- Category: {text(finding.get('category'))}",
        f"- Subtype: {text(finding.get('subtype'))}",
        f"- Severity: {text(finding.get('severity'))}",
        f"- Confidence: {text(finding.get('confidence'))}",
        f"- Target: {target}",
        f"- Human review: {text(finding.get('human_review', 'not_reviewed'))}",
        "",
        "## Standard Context",
        "",
        f"- Standard version: {text(standard.get('version'))}",
        f"- Standard commit: {text(standard.get('commit'))}",
        f"- Rule IDs: {text(standard.get('rule_ids', []))}",
        "",
        "## Summary",
        "",
        text(analysis.get("summary")),
        "",
        "## Expected",
        "",
        text(analysis.get("expected")),
        "",
        "## Observed",
        "",
        text(analysis.get("observed")),
        "",
        "## Impact",
        "",
        text(analysis.get("impact")),
        "",
        "## Suggested Action",
        "",
        text(analysis.get("suggested_change")),
        "",
        "## Evidence",
        "",
        "Raw private transcripts, source code, local paths, private URLs, and secrets are excluded by default.",
        "",
    ]

    if evidence:
        for item in evidence:
            lines.append(f"- {text(item)}")
    else:
        lines.append("- No event-level evidence was exported in this sanitized report.")

    lines.extend(
        [
            "",
            "## Privacy Review",
            "",
            "- [ ] Raw transcripts are excluded.",
            "- [ ] Secrets, local paths, and private URLs are redacted.",
            "- [ ] Public upstream reporting has human approval when applicable.",
            "",
        ]
    )
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("findings")
    parser.add_argument("--output")
    parser.add_argument("--target", choices=["auto", "downstream-project", "upstream-standard"], default="auto")
    parser.add_argument("--max-evidence-events", type=int, default=5)
    args = parser.parse_args()

    findings = read_jsonl(Path(args.findings))
    report = "\n---\n\n".join(
        render_finding(finding, args.target, args.max_evidence_events)
        for finding in findings
    )
    if not report:
        report = "# Runtime AI Finding Report\n\nNo findings were present.\n"

    if args.output:
        output = Path(args.output)
        output.parent.mkdir(parents=True, exist_ok=True)
        with output.open("w", encoding="utf-8", newline="\n") as stream:
            stream.write(report)
        print(f"Wrote report to {output}")
    else:
        print(report)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
