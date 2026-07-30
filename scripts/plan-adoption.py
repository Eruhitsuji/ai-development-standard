#!/usr/bin/env python3
"""Print a conservative adoption plan for an existing downstream project."""

import argparse
from pathlib import Path


ENTRY_PATHS = [
    "AGENTS.md",
    "CLAUDE.md",
    ".kiro/steering",
    ".github/PULL_REQUEST_TEMPLATE.md",
    ".github/ISSUE_TEMPLATE",
    ".github/workflows",
    ".github/CODEOWNERS",
    ".ai",
]


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--project-dir", required=True)
    parser.add_argument("--profiles", nargs="+", default=["core"])
    parser.add_argument("--level", choices=["passive", "guided", "enforced"], default="guided")
    args = parser.parse_args()

    project_dir = Path(args.project_dir).resolve()
    if not project_dir.exists():
        raise SystemExit("Project directory does not exist: " + str(project_dir))

    existing = []
    missing = []
    for relative in ENTRY_PATHS:
        path = project_dir / relative
        if path.exists():
            existing.append(relative)
        else:
            missing.append(relative)

    print("Existing project adoption plan")
    print("Project: " + str(project_dir))
    print("Adoption level: " + args.level)
    print("Profiles: " + ", ".join(args.profiles))
    print("")
    print("Detected existing standard-sensitive paths:")
    for relative in existing:
        print("- preserve and review: " + relative)
    if not existing:
        print("- none")
    print("")
    print("Missing paths that can be added:")
    for relative in missing:
        print("- " + relative)
    print("")
    print("Recommended sequence:")
    print("1. Create an adoption issue from templates/github/ISSUE_TEMPLATE/standard-adoption.yml.")
    print("2. Create branch chore/adopt-ai-development-standard.")
    print("3. Run scripts/init-project.py with --mode existing and selected profiles.")
    print("4. Review .ai/adoption/REPORT.md for preserved files and manual merge items.")
    print("5. Add standard references to existing entry files without deleting project rules.")
    print("6. Run standard validation and known existing project checks.")
    print("7. Open an adoption pull request with remaining foundation issues listed.")
    print("8. Enable stricter branch rules only after validation is stable.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
