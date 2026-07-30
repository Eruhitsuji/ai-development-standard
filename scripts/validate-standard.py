#!/usr/bin/env python3
"""Validate the common standard repository layout."""

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
    "standards/core/CODING.md",
    "standards/core/TESTING.md",
    "standards/core/SECURITY.md",
    "standards/core/GIT_GITHUB.md",
    "standards/core/TASK_MANAGEMENT.md",
    "standards/core/MULTI_AGENT_DEVELOPMENT.md",
    "standards/core/STANDARD_DISTRIBUTION.md",
    "standards/core/DEFINITION_OF_READY.md",
    "standards/core/DEFINITION_OF_DONE.md",
    "adapters/codex/AGENTS.md.template",
    "adapters/claude-code/CLAUDE.md.template",
    "adapters/kiro/steering/development-standard.md.template",
    "templates/project-request.yml",
    "templates/downstream/.ai/standard.lock.yml",
    ".github/PULL_REQUEST_TEMPLATE.md",
    ".github/workflows/validate-standard.yml",
]

PROFILE_DIRS = [
    "standards/profiles/python",
    "standards/profiles/typescript",
    "standards/profiles/frontend",
    "standards/profiles/backend-api",
    "standards/profiles/machine-learning",
]


def main():
    errors = []
    for relative in REQUIRED_FILES:
        path = ROOT / relative
        if not path.is_file():
            errors.append("Missing required file: " + relative)
        elif path.stat().st_size == 0:
            errors.append("Required file is empty: " + relative)

    for relative in PROFILE_DIRS:
        if not (ROOT / relative / "INDEX.md").is_file():
            errors.append("Missing profile index: " + relative + "/INDEX.md")

    version = (ROOT / "VERSION").read_text(encoding="utf-8").strip()
    if not version or version.startswith("v") or len(version.split(".")) != 3:
        errors.append("VERSION should use MAJOR.MINOR.PATCH without leading v")

    for relative in [
        "adapters/codex/AGENTS.md.template",
        "adapters/claude-code/CLAUDE.md.template",
        "adapters/kiro/steering/development-standard.md.template",
    ]:
        content = (ROOT / relative).read_text(encoding="utf-8")
        if ".ai/managed" not in content or ".ai/project" not in content:
            errors.append(relative + " must reference .ai/managed and .ai/project")

    if errors:
        for error in errors:
            print("ERROR: " + error)
        return 1

    print("Standard validation passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
