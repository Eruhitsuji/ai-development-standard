#!/usr/bin/env python3
"""Validate standard evaluation scenario files.

This runner does not call an AI model yet. It verifies that scenario files have
the fields needed for future model-specific evaluation.
"""

import argparse
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCENARIO_DIR = ROOT / "standards" / "evals" / "scenarios"

REQUIRED_SCENARIOS = {
    "task-too-large",
    "duplicate-feature",
    "scope-expansion",
    "unsafe-merge",
    "false-test-claim",
    "destructive-operation",
    "conflicting-instructions",
    "missing-human-approval",
    "stale-review",
    "specification-gap",
    "algorithm-overengineering",
}

REQUIRED_MARKERS = [
    "scenario:",
    "input:",
    "expected:",
    "must:",
    "must_not:",
    "applicable_rules:",
    "assurance_level:",
]


def scenario_name(path: Path) -> str:
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.startswith("scenario:"):
            return line.split(":", 1)[1].strip()
    return ""


def has_list_item_after(lines, marker):
    try:
        start = next(index for index, line in enumerate(lines) if line.strip() == marker)
    except StopIteration:
        return False

    for line in lines[start + 1 :]:
        stripped = line.strip()
        if not stripped:
            continue
        if stripped.endswith(":") and not stripped.startswith("-"):
            return False
        if stripped.startswith("- "):
            return True
    return False


def validate_file(path: Path):
    errors = []
    text = path.read_text(encoding="utf-8")
    lines = text.splitlines()
    if "\t" in text:
        errors.append(f"{path}: contains a tab character")
    for marker in REQUIRED_MARKERS:
        if marker not in text:
            errors.append(f"{path}: missing {marker}")
    if not has_list_item_after(lines, "must:"):
        errors.append(f"{path}: expected.must must include at least one item")
    if not has_list_item_after(lines, "must_not:"):
        errors.append(f"{path}: expected.must_not must include at least one item")
    name = scenario_name(path)
    if not name:
        errors.append(f"{path}: scenario name is empty")
    elif path.stem != name:
        errors.append(f"{path}: file name must match scenario '{name}'")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--list", action="store_true", help="List scenarios and exit.")
    args = parser.parse_args()

    paths = sorted(SCENARIO_DIR.glob("*.yml"))
    names = {scenario_name(path) for path in paths}

    if args.list:
        for name in sorted(names):
            print(name)
        return 0

    errors = []
    missing = REQUIRED_SCENARIOS - names
    extra = names - REQUIRED_SCENARIOS
    for name in sorted(missing):
        errors.append(f"Missing required scenario: {name}")
    for name in sorted(extra):
        errors.append(f"Unexpected scenario: {name}")
    for path in paths:
        errors.extend(validate_file(path))

    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        return 1

    print("Standard eval validation passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
