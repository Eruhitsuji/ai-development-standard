# AI Development Standard

> **Project status:** Experimental Preview. The intended first public release is
> `v0.1.0`. See [Project Status](docs/PROJECT_STATUS.md) for implemented scope,
> limitations, and pre-1.0 stability expectations.

A tool-neutral AI-driven development standard for projects managed on GitHub.

This repository is the upstream source of truth for shared development rules,
AI agent instructions, task management conventions, and project bootstrap/update
flows.

## Start Here

- [Quick Start](docs/QUICKSTART.md)
- [クイックスタート（日本語）](docs/QUICKSTART.ja.md)
- [Project Status and Limitations](docs/PROJECT_STATUS.md)
- [Security Policy](SECURITY.md)
- [Public Release Checklist](docs/PUBLIC_RELEASE_CHECKLIST.md)
- [MIT License](LICENSE)

English is authoritative for the repository. The Japanese Quick Start is a
convenience translation.

## Purpose

This standard is designed for projects where humans, Codex, Claude Code, Kiro,
and other AI tools work together through GitHub Issues, GitHub Projects,
branches, worktrees, pull requests, and CI.

The basic operating rule is:

```text
1 Issue = 1 executor = 1 branch/worktree = 1 pull request
```

## Repository Role

Use this repository as the canonical source for:

- shared development, testing, security, and GitHub standards
- multi-human and multi-AI parallel development rules
- GitHub Issues/Projects based task management
- downstream `.ai/managed` and `.ai/project` separation
- local-first runtime evidence collection from AI development history
- Codex, Claude Code, and Kiro adapter templates
- new project initialization flow
- existing project adoption flow
- next-action guidance for users who do not know what to do next
- development method selection beyond only agile or W-model
- risk-based assurance levels across Quick, Standard, High, and Regulated work
- full lifecycle coverage from discovery through operations, incidents,
  deprecation, and retirement
- traceability and capability management to prevent duplicate or missing work
- AI-human interaction rules for recommendations, decision requests, blockers,
  approvals, and completion guidance
- standard update flow
- Issue and pull request templates
- GitHub Actions starter workflows
- standard versioning and distribution rules

## Downstream Model

Each project receives a fixed snapshot of the standard.

```text
ai-development-standard
        |
        | release tag + commit SHA
        v
project/.ai/managed/
        |
        +-- project/.ai/project/
        |
        +-- AGENTS.md / CLAUDE.md / .kiro/steering/
```

Do not make downstream AI tools read an untracked local copy of this repository.
The project-local snapshot must be committed, reviewable, and version-locked.

## Main Directories

```text
standards/core/          Required shared standards
standards/evals/         Model-neutral standard evaluation scenarios
standards/evals/runtime/ Runtime evidence evaluation scenarios
standards/profiles/      Optional technology/domain profiles
agents/roles/            Role definitions for humans and AI agents
agents/policies/         Cross-agent execution policies
adapters/                Codex, Claude Code, and Kiro entry templates
docs/flows/              New project, development, and update flows
templates/               Downstream project templates
schemas/                 Configuration schemas
scripts/                 Bootstrap and validation helpers
.github/                 Issue templates, PR template, and workflow examples
```

## Common Quality Areas

The shared baseline defines these project-independent quality areas:

- process: method-independent lifecycle with explicit quality gates
- methods: Kanban, Scrum, Scrumban, Waterfall, V-model, W-model, XP, Lean,
  dual-track agile, Shape Up, Spiral, prototype/PoC, trunk-based development,
  release train, maintenance, and regulated flows
- assurance: Quick, Standard, High, and Regulated levels selected by risk,
  change type, evidence needs, and required human approvals
- specification consistency: living specs plus change packages for
  requirements, design, traceability, decisions, and verification
- task decomposition: XS/S preferred, M requires reason, L/XL cannot be Ready
- capability management: registry, reuse check, duplicate detection,
  deprecation, and replacement records
- traceability: Requirement -> Capability -> Epic -> Task -> PR ->
  Test/Evidence -> Release
- guidance: AI-assisted current-state diagnosis and next-action recommendation
- runtime evidence: local-first AI history collection, provider-neutral
  normalized events, deterministic findings, sanitized reporting, and upstream
  standard feedback loops
- AI compatibility: shared execution contract across Codex, Claude Code, Kiro,
  and future tools
- AI-human interaction: concise recommendations, one to three questions, and
  explicit decision requests for human-only approvals
- merge governance: stale-review detection, merge authority separation,
  shared-file ownership, rollback/revert confirmation, and Ruleset safety
- review: requirements, design, code, test, security, integration, and release
  viewpoints
- testing: acceptance, normal path, edge, error, compatibility, security, data,
  concurrency, observability, and performance viewpoints
- coding: readability, cohesion, coupling, testability, compatibility, error
  handling, observability, performance, and deletion safety
- security: assets, trust boundaries, authentication, authorization, input and
  output handling, secrets, dependencies, data protection, auditability, and
  least privilege

## Adoption Modes

Use one of two adoption modes.

| Mode | Use When | Primary Flow |
| --- | --- | --- |
| New project | The repository is being created from scratch | `docs/flows/NEW_PROJECT.md` |
| Existing project | The repository already has code, CI, issues, or team rules | `docs/flows/EXISTING_PROJECT_ADOPTION.md` |

Both modes install a committed standard snapshot under `.ai/managed` and keep
project-specific rules under `.ai/project`. Existing projects add the standard
in stages and preserve current CI, templates, and AI instructions unless a
reviewed adoption pull request changes them.

## New Project Flow

1. Create a new repository from `ai-project-template`.
2. Select this standard's release tag and commit SHA.
3. Install only required core/profile files into `.ai/managed`.
4. Generate project-specific files under `.ai/project`.
5. Generate AI entry files: `AGENTS.md`, `CLAUDE.md`, and `.kiro/steering`.
6. Create or link a GitHub Project from the organization template.
7. Create the initialization pull request.
8. Complete foundation issues before normal feature work starts.

See [docs/flows/NEW_PROJECT.md](docs/flows/NEW_PROJECT.md).
Use `templates/foundation-issues/new-project.md` for the initial foundation
Epic.

## Existing Project Adoption Flow

1. Audit existing project structure, CI, owners, issue templates, PR templates,
   and AI instruction files.
2. Create an adoption issue from
   `templates/github/ISSUE_TEMPLATE/standard-adoption.yml`.
3. Create an adoption branch such as `chore/adopt-ai-development-standard`.
4. Install the standard snapshot into `.ai/managed`.
5. Create project-specific files under `.ai/project` with TODOs where details
   are not yet known.
6. Preserve existing files and manually merge standard references where needed.
7. Open an adoption pull request and create follow-up foundation issues.

See
[docs/flows/EXISTING_PROJECT_ADOPTION.md](docs/flows/EXISTING_PROJECT_ADOPTION.md).
Use `templates/foundation-issues/existing-project-adoption.md` for the adoption
foundation Epic.

## Standard Update Flow

1. Change this repository through an issue and pull request.
2. Release a new standard version.
3. Open update pull requests in downstream projects.
4. Update `.ai/managed` and `.ai/standard.lock.yml`.
5. Validate project-specific overrides and exceptions.
6. Merge after the project owner and standard owner approve.

See [docs/flows/STANDARD_UPDATE.md](docs/flows/STANDARD_UPDATE.md).

## When You Do Not Know What To Do Next

Ask the AI "what should I do next?" The AI should inspect the current project
state, classify the phase, and recommend the next one to three actions using
`standards/core/NEXT_ACTION.md`.

Typical outputs are:

- a guidance answer
- a refined GitHub Issue
- a process decision
- an implementation plan
- a review or test plan
- a blocker to resolve

Use `templates/next-action-report.md` for longer recommendations.

## Validation

Run:

```bash
python scripts/validate-standard.py
python scripts/run-standard-evals.py
python scripts/check-public-release.py
```

The standard validator checks required files, profiles, adapters, and core
template consistency. The evaluation runner checks that required AI behavior
scenarios contain expected `must` and `must_not` outcomes. The public-release
check validates public documentation and scans current tracked text files for a
small set of high-confidence secret patterns.

The public-release check does not scan Git history, Issues, pull requests,
workflow logs, artifacts, forks, or caches. Follow
[the full release checklist](docs/PUBLIC_RELEASE_CHECKLIST.md) before changing
repository visibility or publishing a tag.

Runtime evidence tooling is available for local preview use:

```bash
python scripts/export-ai-history.py --project-dir ../project --output ai-development-history.jsonl
python scripts/analyze-ai-history.py ai-development-history.jsonl --output ai-history-findings.jsonl
python scripts/report-ai-findings.py ai-history-findings.jsonl --output ai-finding-report.md
```

The exporter omits raw provider content unless `--include-raw` is explicitly
provided. Generated reports are sanitized summaries and do not create GitHub
Issues automatically.

Run the combined local check:

```bash
./scripts/check.sh
```

On PowerShell:

```powershell
.\scripts\check.ps1
```

For an existing downstream repository, first inspect the expected adoption work:

```bash
python scripts/plan-adoption.py --project-dir ../existing-project --profiles core python
```

Then install the snapshot conservatively:

```bash
python scripts/init-project.py --project-dir ../existing-project --mode existing --commit <standard-commit-sha> --profiles core python
```

## Public Preview Expectations

The intended `v0.1.0` release is an Experimental Preview. It is suitable for
pilots and reviewed adoption, but it does not yet automate live model
evaluation, GitHub Projects and Rulesets, release retrieval, or downstream
standard-update pull requests. Pin both the version and commit SHA, and review
updates through dedicated pull requests.

See [Project Status](docs/PROJECT_STATUS.md) for details.

## Versioning

Use semantic versioning:

- patch: clarifications and non-breaking fixes
- minor: additive rules, profiles, templates, and checks
- major: priority changes, required workflow changes, or manual migrations

The current version is stored in [VERSION](VERSION).

## License

This project is licensed under the [MIT License](LICENSE).
