# AGENTS.md

This repository defines the shared AI-driven development standard.

## Authoritative Sources

Read these before changing the standard:

1. `README.md`
2. `standards/core/INDEX.md`
3. `standards/core/PROCESS.md`
4. `standards/core/DEVELOPMENT_METHODS.md`
5. `standards/core/NEXT_ACTION.md`
6. `standards/core/AI_TOOL_COMPATIBILITY.md`
7. `standards/core/REVIEW.md`
8. `docs/flows/OVERALL_FLOW.md`
9. `docs/flows/NEW_PROJECT.md`
10. `docs/flows/EXISTING_PROJECT_ADOPTION.md`
11. `docs/flows/STANDARD_UPDATE.md`
12. `.ai/project/PROJECT.yml`
13. `.ai/project/METHOD.yml`
14. `.ai/project/GUIDANCE.yml`
15. `.ai/project/COMMANDS.yml`

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

## Repository Ownership Rules

- `standards/**`, `agents/**`, `adapters/**`, `schemas/**`, and `scripts/**`
  are upstream standard source files.
- `templates/downstream/.ai/managed/**` represents generated downstream output.
- Project-specific downstream rules must go under `.ai/project/**`, not
  `.ai/managed/**`.
- Changes to standard behavior require a changelog entry and versioning decision.

## Required Workflow

Before implementation:

1. Identify the target issue or requested scope.
2. Inspect related standard files and templates.
3. Decide whether the change is patch, minor, or major.
4. Identify downstream compatibility impact.
5. Identify affected process, review, test, coding, and security viewpoints.

During implementation:

- Make the smallest coherent change.
- Avoid unrelated refactoring.
- Keep adapter templates aligned with core standard changes.
- Update schemas, docs, scripts, and templates together when contracts change.
- Preserve method-independent lifecycle gates unless explicitly changing the
  process standard.

After implementation:

1. Run `python scripts/validate-standard.py`.
2. Inspect the complete diff.
3. Update `CHANGELOG.md` when behavior or files change.
4. Report verification results and remaining risks.

## Prohibited Actions

Do not:

- weaken security requirements without explicit approval
- edit downstream generated snapshots as if they were the upstream source
- invent project-specific rules inside common standards
- claim validation passed unless it was executed
- force-push or rewrite another contributor's branch without approval
