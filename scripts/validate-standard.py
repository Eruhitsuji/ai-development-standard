#!/usr/bin/env python3
"""Validate the common standard repository layout.

The script intentionally uses only the Python standard library so it can run in
fresh repositories and GitHub Actions without dependency setup.
"""

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
    "docs/flows/OVERALL_FLOW.md",
    "docs/flows/NEW_PROJECT.md",
    "docs/flows/EXISTING_PROJECT_ADOPTION.md",
    "docs/flows/NORMAL_DEVELOPMENT.md",
    "docs/flows/STANDARD_UPDATE.md",
    "standards/core/INDEX.md",
    "standards/core/DEVELOPMENT.md",
    "standards/core/PROCESS.md",
    "standards/core/DEVELOPMENT_METHODS.md",
    "standards/core/NEXT_ACTION.md",
    "standards/core/AI_TOOL_COMPATIBILITY.md",
    "standards/core/REVIEW.md",
    "standards/core/CODING.md",
    "standards/core/TESTING.md",
    "standards/core/SECURITY.md",
    "standards/core/GIT_GITHUB.md",
    "standards/core/TASK_MANAGEMENT.md",
    "standards/core/MULTI_AGENT_DEVELOPMENT.md",
    "standards/core/STANDARD_DISTRIBUTION.md",
    "standards/core/DEFINITION_OF_READY.md",
    "standards/core/DEFINITION_OF_DONE.md",
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
    "templates/handoff.md",
    "templates/foundation-issues/README.md",
    "templates/foundation-issues/new-project.md",
    "templates/foundation-issues/existing-project-adoption.md",
    "templates/downstream/.ai/standard.lock.yml",
    "templates/downstream/.ai/project/PROJECT.yml",
    "templates/downstream/.ai/project/METHOD.yml",
    "templates/downstream/.ai/project/GUIDANCE.yml",
    "templates/downstream/.ai/project/COMMANDS.yml",
    "templates/github/ISSUE_TEMPLATE/standard-adoption.yml",
    "templates/github/ISSUE_TEMPLATE/guidance.yml",
    "templates/github/ISSUE_TEMPLATE/process-decision.yml",
    ".github/PULL_REQUEST_TEMPLATE.md",
    ".github/workflows/validate-standard.yml",
    "scripts/plan-adoption.py",
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
        ]:
            if standard not in content:
                errors.append(f"{label} does not reference {standard}")


def main() -> int:
    errors = []
    check_required_files(errors)
    check_profiles(errors)
    check_version(errors)
    check_adapter_consistency(errors)

    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        return 1

    print("Standard validation passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
