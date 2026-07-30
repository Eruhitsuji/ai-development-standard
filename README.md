# AI Development Standard

AI-driven development standard for projects managed on GitHub.

This repository is the upstream source of truth for shared development rules,
AI agent instructions, task management conventions, and project bootstrap/update
flows.

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
- Codex, Claude Code, and Kiro adapter templates
- new project initialization flow
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

- process: agile delivery loop with W-model quality gates
- review: requirements, design, code, test, security, integration, and release
  viewpoints
- testing: acceptance, normal path, edge, error, compatibility, security, data,
  concurrency, observability, and performance viewpoints
- coding: readability, cohesion, coupling, testability, compatibility, error
  handling, observability, performance, and deletion safety
- security: assets, trust boundaries, authentication, authorization, input and
  output handling, secrets, dependencies, data protection, auditability, and
  least privilege

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

## Standard Update Flow

1. Change this repository through an issue and pull request.
2. Release a new standard version.
3. Open update pull requests in downstream projects.
4. Update `.ai/managed` and `.ai/standard.lock.yml`.
5. Validate project-specific overrides and exceptions.
6. Merge after the project owner and standard owner approve.

See [docs/flows/STANDARD_UPDATE.md](docs/flows/STANDARD_UPDATE.md).

## Validation

Run:

```bash
python scripts/validate-standard.py
```

The validation script checks the presence of required files and basic adapter
consistency.

## Versioning

Use semantic versioning:

- patch: clarifications and non-breaking fixes
- minor: additive rules, profiles, templates, and checks
- major: priority changes, required workflow changes, or manual migrations

The current version is stored in [VERSION](VERSION).
