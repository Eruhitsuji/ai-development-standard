#!/usr/bin/env python3
"""Validate the common standard repository layout.

The script intentionally uses only the Python standard library so it can run in
fresh repositories and GitHub Actions without dependency setup.
"""

import ast
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


REQUIRED_FILES = [
    "README.md",
    "VERSION",
    "CHANGELOG.md",
    "AGENTS.md",
    "CLAUDE.md",
    ".ai/project/METHOD.yml",
    ".ai/project/GUIDANCE.yml",
    "schemas/project.schema.yml",
    "schemas/standard-lock.schema.yml",
    "schemas/task-contract.schema.yml",
    "schemas/method.schema.yml",
    "schemas/guidance.schema.yml",
    "schemas/context-index.schema.yml",
    "schemas/capabilities.schema.yml",
    "schemas/traceability.schema.yml",
    "schemas/assurance.schema.yml",
    "schemas/roles.schema.yml",
    "schemas/merge-policy.schema.yml",
    "schemas/change-package.schema.yml",
    "schemas/review-ledger.schema.yml",
    "schemas/ai-history-archive.schema.yml",
    "schemas/ai-history-event.schema.yml",
    "schemas/ai-finding.schema.yml",
    "schemas/runtime-evidence-config.schema.yml",
    "docs/flows/OVERALL_FLOW.md",
    "docs/flows/NEW_PROJECT.md",
    "docs/flows/EXISTING_PROJECT_ADOPTION.md",
    "docs/flows/NORMAL_DEVELOPMENT.md",
    "docs/flows/STANDARD_UPDATE.md",
    "standards/core/INDEX.md",
    "standards/core/DEVELOPMENT.md",
    "standards/core/PROCESS.md",
    "standards/core/DEVELOPMENT_METHODS.md",
    "standards/core/SPECIFICATION_LIFECYCLE.md",
    "standards/core/ARTIFACT_CONSISTENCY.md",
    "standards/core/ASSURANCE_LEVELS.md",
    "standards/core/NEXT_ACTION.md",
    "standards/core/AI_TOOL_COMPATIBILITY.md",
    "standards/core/AI_HUMAN_INTERACTION.md",
    "standards/core/AI_PERMISSIONS.md",
    "standards/core/REVIEW.md",
    "standards/core/CODING.md",
    "standards/core/TESTING.md",
    "standards/core/SECURITY.md",
    "standards/core/GIT_GITHUB.md",
    "standards/core/MERGE_GOVERNANCE.md",
    "standards/core/TASK_MANAGEMENT.md",
    "standards/core/TASK_DECOMPOSITION.md",
    "standards/core/TRACEABILITY.md",
    "standards/core/CAPABILITY_MANAGEMENT.md",
    "standards/core/MULTI_AGENT_DEVELOPMENT.md",
    "standards/core/OPERATIONS.md",
    "standards/core/AUTOMATION_AND_HOOKS.md",
    "standards/core/KNOWLEDGE_MAINTENANCE.md",
    "standards/core/STANDARD_DISTRIBUTION.md",
    "standards/core/STANDARD_EVALUATION.md",
    "standards/core/RUNTIME_EVIDENCE.md",
    "standards/core/DEFINITION_OF_READY.md",
    "standards/core/DEFINITION_OF_DONE.md",
    "standards/evals/README.md",
    "standards/evals/scenarios/task-too-large.yml",
    "standards/evals/scenarios/duplicate-feature.yml",
    "standards/evals/scenarios/scope-expansion.yml",
    "standards/evals/scenarios/unsafe-merge.yml",
    "standards/evals/scenarios/false-test-claim.yml",
    "standards/evals/scenarios/destructive-operation.yml",
    "standards/evals/scenarios/conflicting-instructions.yml",
    "standards/evals/scenarios/missing-human-approval.yml",
    "standards/evals/scenarios/stale-review.yml",
    "standards/evals/scenarios/specification-gap.yml",
    "standards/evals/scenarios/algorithm-overengineering.yml",
    "standards/evals/runtime/process.yml",
    "standards/evals/runtime/ai-human.yml",
    "standards/evals/runtime/issue-workflow.yml",
    "standards/evals/runtime/security.yml",
    "standards/evals/runtime/efficiency.yml",
    "standards/evals/runtime/fixtures/README.md",
    "standards/evals/runtime/fixtures/synthetic-history.jsonl",
    "agents/roles/orchestrator.md",
    "agents/roles/implementer.md",
    "agents/roles/reviewer.md",
    "agents/roles/integrator.md",
    "adapters/codex/AGENTS.md.template",
    "adapters/claude-code/CLAUDE.md.template",
    "adapters/kiro/steering/development-standard.md.template",
    "templates/project-request.yml",
    "templates/existing-project-adoption.yml",
    "templates/project-discovery.md",
    "templates/process-selection.md",
    "templates/next-action-report.md",
    "templates/task-contract.md",
    "templates/implementation-plan.md",
    "templates/review-report.md",
    "templates/test-plan.md",
    "templates/security-review.md",
    "templates/investigation-report.md",
    "templates/algorithm-decision.md",
    "templates/ai-history-collection-plan.md",
    "templates/ai-finding-report.md",
    "templates/operations-change.md",
    "templates/incident-report.md",
    "templates/deprecation-plan.md",
    "templates/review-ledger.md",
    "templates/release-checklist.md",
    "templates/handoff.md",
    "templates/foundation-issues/README.md",
    "templates/foundation-issues/new-project.md",
    "templates/foundation-issues/existing-project-adoption.md",
    "templates/downstream/.ai/standard.lock.yml",
    "templates/downstream/.ai/project/PROJECT.yml",
    "templates/downstream/.ai/project/METHOD.yml",
    "templates/downstream/.ai/project/GUIDANCE.yml",
    "templates/downstream/.ai/project/COMMANDS.yml",
    "templates/downstream/.ai/project/CONTEXT_INDEX.yml",
    "templates/downstream/.ai/project/CAPABILITIES.yml",
    "templates/downstream/.ai/project/TRACEABILITY.yml",
    "templates/downstream/.ai/project/ASSURANCE.yml",
    "templates/downstream/.ai/project/ROLES.yml",
    "templates/downstream/.ai/project/MERGE_POLICY.yml",
    "templates/downstream/.ai/project/PERMISSIONS.yml",
    "templates/downstream/.ai/project/AI_HISTORY.yml",
    "templates/downstream/.ai/project/LIFECYCLE.yml",
    "templates/downstream/.ai/project/changes/README.md",
    "templates/downstream/.ai/project/changes/_template/change.yml",
    "templates/downstream/.ai/project/changes/_template/requirements.yml",
    "templates/downstream/.ai/project/changes/_template/design.md",
    "templates/downstream/.ai/project/changes/_template/traceability.yml",
    "templates/downstream/.ai/project/changes/_template/decisions.md",
    "templates/downstream/.ai/project/changes/_template/verification.yml",
    "templates/github/ISSUE_TEMPLATE/standard-adoption.yml",
    "templates/github/ISSUE_TEMPLATE/guidance.yml",
    "templates/github/ISSUE_TEMPLATE/process-decision.yml",
    "templates/github/ISSUE_TEMPLATE/task.yml",
    "templates/github/ISSUE_TEMPLATE/feature.yml",
    "templates/github/ISSUE_TEMPLATE/investigation.yml",
    "templates/github/ISSUE_TEMPLATE/algorithm-decision.yml",
    "templates/github/ISSUE_TEMPLATE/operations-change.yml",
    "templates/github/ISSUE_TEMPLATE/incident.yml",
    "templates/github/ISSUE_TEMPLATE/deprecation.yml",
    "templates/github/ISSUE_TEMPLATE/runtime-finding.yml",
    ".github/PULL_REQUEST_TEMPLATE.md",
    ".github/workflows/validate-standard.yml",
    "scripts/plan-adoption.py",
    "scripts/run-standard-evals.py",
    "scripts/export-ai-history.py",
    "scripts/analyze-ai-history.py",
    "scripts/report-ai-findings.py",
]


REQUIRED_PROFILE_DIRS = [
    "standards/profiles/python",
    "standards/profiles/typescript",
    "standards/profiles/frontend",
    "standards/profiles/backend-api",
    "standards/profiles/machine-learning",
]


def read_text(path):
    return (ROOT / path).read_text(encoding="utf-8")


def check_required_files(errors):
    for relative in REQUIRED_FILES:
        path = ROOT / relative
        if not path.is_file():
            errors.append(f"Missing required file: {relative}")
            continue
        if path.stat().st_size == 0 and path.name != ".gitkeep":
            errors.append(f"Required file is empty: {relative}")


def check_profiles(errors):
    for relative in REQUIRED_PROFILE_DIRS:
        index = ROOT / relative / "INDEX.md"
        if not index.is_file():
            errors.append(f"Missing profile index: {relative}/INDEX.md")


def check_version(errors):
    version = read_text("VERSION").strip()
    if not version:
        errors.append("VERSION is empty")
    if version.startswith("v"):
        errors.append("VERSION must not include the leading v")
    if len(version.split(".")) != 3:
        errors.append("VERSION should use MAJOR.MINOR.PATCH")


def check_adapter_consistency(errors):
    codex = read_text("adapters/codex/AGENTS.md.template")
    claude = read_text("adapters/claude-code/CLAUDE.md.template")
    kiro = read_text("adapters/kiro/steering/development-standard.md.template")
    for label, content in {
        "Codex adapter": codex,
        "Claude Code adapter": claude,
        "Kiro adapter": kiro,
    }.items():
        if ".ai/managed" not in content:
            errors.append(f"{label} does not reference .ai/managed")
        if ".ai/project" not in content:
            errors.append(f"{label} does not reference .ai/project")
        for standard in [
            "DEVELOPMENT_METHODS.md",
            "NEXT_ACTION.md",
            "AI_TOOL_COMPATIBILITY.md",
            "ASSURANCE_LEVELS.md",
            "TRACEABILITY.md",
            "CAPABILITY_MANAGEMENT.md",
            "MERGE_GOVERNANCE.md",
            "AI_HUMAN_INTERACTION.md",
            "RUNTIME_EVIDENCE.md",
        ]:
            if standard not in content:
                errors.append(f"{label} does not reference {standard}")
        if "CONTEXT_INDEX.yml" not in content:
            errors.append(f"{label} does not reference CONTEXT_INDEX.yml")
        if "AI_HISTORY.yml" not in content:
            errors.append(f"{label} does not reference AI_HISTORY.yml")


def check_no_tabs(errors):
    for relative in REQUIRED_FILES:
        path = ROOT / relative
        if path.is_file() and "\t" in path.read_text(encoding="utf-8"):
            errors.append(f"File contains tab characters: {relative}")


def check_context_index(errors):
    content = read_text("templates/downstream/.ai/project/CONTEXT_INDEX.yml")
    for marker in [
        "id:",
        "load_when:",
        "applies_to:",
        "severity:",
        "required_action:",
        "human_interaction_type:",
        "overridable:",
    ]:
        if marker not in content:
            errors.append(f"CONTEXT_INDEX.yml missing marker: {marker}")
    if "CTX-RUNTIME-001" not in content:
        errors.append("CONTEXT_INDEX.yml missing CTX-RUNTIME-001")


def check_runtime_evidence_config(errors):
    content = read_text("templates/downstream/.ai/project/AI_HISTORY.yml")
    for marker in [
        "runtime_evidence:",
        "default_mode:",
        "raw_content:",
        "automatic_upstream_reporting:",
        "require_human_approval:",
        "ADS-FINDING",
    ]:
        if marker not in content:
            errors.append(f"AI_HISTORY.yml missing marker: {marker}")


def check_python_scripts_parse(errors):
    for relative in [
        "scripts/validate-standard.py",
        "scripts/run-standard-evals.py",
        "scripts/plan-adoption.py",
        "scripts/init-project.py",
        "scripts/check-public-release.py",
        "scripts/export-ai-history.py",
        "scripts/analyze-ai-history.py",
        "scripts/report-ai-findings.py",
    ]:
        path = ROOT / relative
        try:
            ast.parse(path.read_text(encoding="utf-8"), filename=relative)
        except SyntaxError as exc:
            errors.append(f"{relative}: syntax error: {exc}")


def check_capability_ids(errors):
    content = read_text("templates/downstream/.ai/project/CAPABILITIES.yml")
    ids = []
    for line in content.splitlines():
        stripped = line.strip()
        if stripped.startswith("- id:"):
            ids.append(stripped.split(":", 1)[1].strip())
    duplicates = sorted({item for item in ids if ids.count(item) > 1})
    for duplicate in duplicates:
        errors.append(f"Duplicate capability id in template: {duplicate}")


def check_change_package_template(errors):
    required = [
        "change.yml",
        "requirements.yml",
        "design.md",
        "traceability.yml",
        "decisions.md",
        "verification.yml",
    ]
    base = ROOT / "templates" / "downstream" / ".ai" / "project" / "changes" / "_template"
    for name in required:
        path = base / name
        if not path.is_file():
            errors.append(f"Missing change package template file: {name}")


def main() -> int:
    errors = []
    check_required_files(errors)
    check_profiles(errors)
    check_version(errors)
    check_adapter_consistency(errors)
    check_no_tabs(errors)
    check_context_index(errors)
    check_runtime_evidence_config(errors)
    check_capability_ids(errors)
    check_change_package_template(errors)
    check_python_scripts_parse(errors)

    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        return 1

    print("Standard validation passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
