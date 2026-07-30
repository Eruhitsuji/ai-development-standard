# AGENTS.md

This repository defines the shared AI-driven development standard.

## Authoritative Sources

Read these before changing the standard:

1. `README.md`
2. `standards/core/INDEX.md`
3. `docs/flows/OVERALL_FLOW.md`
4. `docs/flows/NEW_PROJECT.md`
5. `docs/flows/STANDARD_UPDATE.md`
6. `.ai/project/PROJECT.yml`
7. `.ai/project/COMMANDS.yml`

## Instruction Priority

When instructions conflict, follow this order:

1. Security and secret-handling rules
2. Explicit user instruction for the current task
3. Approved GitHub issue or pull request scope
4. Non-overridable standard rules
5. Project-specific rules under `.ai/project`
6. Core standards under `standards/core`
7. Profile standards under `standards/profiles`
8. Existing repository patterns

Do not silently resolve material conflicts. Report them before proceeding.

## Required Workflow

Before implementation:

1. Identify the target issue or requested scope.
2. Inspect related standard files and templates.
3. Decide whether the change is patch, minor, or major.
4. Identify downstream compatibility impact.

After implementation:

1. Run `python scripts/validate-standard.py`.
2. Inspect the complete diff.
3. Update `CHANGELOG.md` when behavior or files change.
4. Report verification results and remaining risks.

## Prohibited Actions

Do not weaken security requirements, edit generated snapshots as upstream source, invent project-specific rules inside common standards, or claim validation passed unless it was executed.
