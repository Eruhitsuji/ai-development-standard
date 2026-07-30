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
    "standards/core/INDEX.md",
    "standards/core/DEVELOPMENT.md",
    "standards/core/PROCESS.md",
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
    "templates/downstream/.ai/standard.lock.yml",
    "templates/downstream/.ai/project/PROJECT.yml",
    "templates/downstream/.ai/project/COMMANDS.yml",
    ".github/PULL_REQUEST_TEMPLATE.md",
    ".github/workflows/validate-standard.yml",
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
