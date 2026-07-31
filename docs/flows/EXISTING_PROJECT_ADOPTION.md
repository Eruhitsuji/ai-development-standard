# Existing Project Adoption Flow

Use this flow when an existing GitHub repository should adopt this standard
after code, issues, workflows, or team conventions already exist.

Existing projects are not treated like new projects. Adoption must preserve
working behavior first, then add standardization in reviewable stages.

## Principle

Adopt the standard in layers:

```text
Audit existing project
  -> create adoption issue
  -> create adoption branch
  -> install .ai/managed snapshot
  -> add .ai/project project-specific files
  -> add context index, capability registry, traceability, assurance, roles, and merge policy
  -> add or align AI entry files
  -> add validation and templates without overwriting existing workflows
  -> open adoption pull request
  -> create foundation alignment issues
  -> activate normal development flow
```

The first adoption pull request should be infrastructure and documentation only.
Do not mix adoption with product features, dependency migrations, formatting
sweeps, or large refactoring.

## Inputs

Create an adoption request from `templates/existing-project-adoption.yml`.
Use `templates/foundation-issues/existing-project-adoption.md` for the
foundation Epic after the adoption issue is accepted.

At minimum, collect:

- repository owner, name, and default branch
- current production or release status
- selected standard version and commit SHA
- selected profiles
- existing languages, runtimes, package managers, and CI commands
- existing `AGENTS.md`, `CLAUDE.md`, `.kiro/`, `.github/`, or CODEOWNERS files
- existing capabilities, duplicate features, shared modules, and public APIs
- existing release, deployment, monitoring, incident, or deprecation practices
- maintainer, project owner, technical owners, and reviewers
- open pull requests, release freezes, or risky active work
- desired activation level

## Adoption Levels

| Level | Meaning | Typical Use |
| --- | --- | --- |
| Passive | Install standard docs and AI entry references only | Evaluation or low-risk introduction |
| Guided | Add issue/PR templates and validation workflow | Team starts using the standard for new work |
| Enforced | Add branch rules, CODEOWNERS, required checks, and scope checks | Standard becomes required for normal development |

Start existing projects at `Passive` or `Guided`. Move to `Enforced` only after
CI and ownership are stable.

## Flow

1. Create a standard adoption issue.
2. Audit the repository.
3. Choose adoption level and profiles.
4. Create `chore/adopt-ai-development-standard`.
5. Install `.ai/managed/**` and `.ai/standard.lock.yml`.
6. Generate missing `.ai/project/**` files with TODO values where needed.
7. Initialize `CONTEXT_INDEX.yml`, `CAPABILITIES.yml`, `TRACEABILITY.yml`,
   `ASSURANCE.yml`, `ROLES.yml`, `MERGE_POLICY.yml`, `PERMISSIONS.yml`, and
   `LIFECYCLE.yml`.
8. Preserve existing AI entry files and CI files.
9. Add missing references to the standard manually when an entry file already
   exists.
10. Add issue and pull request templates only when they do not conflict with
   existing templates.
11. Run standard validation and existing project checks that are already known.
12. Open an adoption pull request.
13. Create foundation alignment issues for anything still TODO.
14. Enable stricter rules only after the adoption pull request is merged.

## Existing File Handling

| Existing Path | Default Handling |
| --- | --- |
| `AGENTS.md` | preserve; add standard references manually |
| `CLAUDE.md` | preserve; add standard references manually |
| `.kiro/steering/**` | preserve; add missing generated steering files only after review |
| `.github/workflows/**` | preserve; add validation workflow as a separate file |
| `.github/PULL_REQUEST_TEMPLATE.md` | preserve; merge standard sections manually |
| `.github/ISSUE_TEMPLATE/**` | preserve; add new forms only if names do not conflict |
| `.github/CODEOWNERS` | preserve; align with `.ai/project/OWNERS.yml` in a follow-up |
| `.ai/project/**` | create if missing; project owns these files |
| `.ai/managed/**` | replace only through adoption or standard-update tasks |

## Required Foundation Issues

After adoption, create issues for unfinished alignment work:

- confirm product and project ownership
- document architecture and directory structure
- define setup, format, lint, test, and full-check commands
- align CODEOWNERS and `.ai/project/OWNERS.yml`
- define write scopes for active modules
- initialize the capability registry and mark unknown areas as TODO
- create traceability records for active epics and important features
- select default assurance levels for project change types
- define human-only approval owners for merge, release, deployment, rollback,
  security exceptions, and data deletion
- migrate or add issue templates
- migrate or add pull request template sections
- add or stabilize CI
- decide when branch rules and required checks become enforced
- review open pull requests against the adopted baseline

## Activation Gate

Normal development under this standard starts when:

- adoption pull request is merged
- `.ai/standard.lock.yml` records standard version and commit SHA
- `.ai/managed/**` exists and is not manually edited
- `.ai/project/PROJECT.yml` names the project and owner
- `.ai/project/COMMANDS.yml` has real commands or approved TODO exceptions
- `AGENTS.md` and any enabled AI tool entries point to `.ai/managed` and
  `.ai/project`
- at least one validation command succeeds
- remaining gaps are tracked as issues

## Prohibited During Adoption

Do not:

- rewrite repository history
- reformat unrelated source files
- replace existing CI without a rollback path
- enforce new branch rules before the project can pass required checks
- delete existing issue or pull request templates without review
- mark the project as active while required foundation gaps are untracked
