# AI History Collection Plan

## Purpose

## Target Project

- Repository:
- Project directory:
- Standard version:
- Standard commit:

## Providers

- [ ] Codex
- [ ] Claude Code
- [ ] Kiro
- [ ] Other:

## Collection Mode

- [ ] Metadata only
- [ ] Raw local-only archive
- [ ] Disabled

## Project Association

- Matching mode: exact root / root or child
- Allowed provider roots:
- Text fallback allowed: yes / no

## Privacy Controls

- Raw transcript upload allowed: no
- Redaction required before reporting: yes
- Public upstream issue evidence: sanitized summary only
- Archive location:
- Retention:

## Checks To Run

- [ ] Weak project association
- [ ] Work before Ready
- [ ] Write-scope violation
- [ ] Missing human approval
- [ ] Repeated command failure
- [ ] Context loading or workflow friction
- [ ] Tool compatibility issue

## Reporting

- Downstream project findings:
- Upstream standard findings:
- Human approval owner:
- Deduplication marker: `ADS-FINDING:`

## Commands

```bash
python scripts/export-ai-history.py --project-dir <project-dir> --output ai-development-history.jsonl
python scripts/analyze-ai-history.py ai-development-history.jsonl --output ai-history-findings.jsonl
python scripts/report-ai-findings.py ai-history-findings.jsonl --output ai-finding-report.md
```

## Human Decisions Required

## Remaining Risks
