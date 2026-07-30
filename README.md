# AI Development Standard

AI-driven development standard for projects managed on GitHub.

This repository is the upstream source of truth for shared development rules, AI agent instructions, task management conventions, and project bootstrap/update flows.

## Purpose

This standard is designed for projects where humans, Codex, Claude Code, Kiro, and other AI tools work together through GitHub Issues, GitHub Projects, branches, worktrees, pull requests, and CI.

The basic operating rule is:

```text
1 Issue = 1 executor = 1 branch/worktree = 1 pull request
```

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
        +-- AGENTS.md / CLAUDE.md / .kiro/steering/
```

Do not make downstream AI tools read an untracked local copy of this repository. The project-local snapshot must be committed, reviewable, and version-locked.

## Main Directories

```text
standards/core/          Required shared standards
standards/profiles/      Optional technology/domain profiles
agents/                  Role definitions and policies
adapters/                Codex, Claude Code, and Kiro entry templates
docs/flows/              New project, development, and update flows
templates/               Downstream project starter files
schemas/                 Configuration schemas
scripts/                 Bootstrap and validation helpers
.github/                 Issue templates, PR template, and workflow examples
```

## New Project Flow

1. Create a new repository from `ai-project-template`.
2. Select this standard's release tag and commit SHA.
3. Install required core/profile files into `.ai/managed`.
4. Generate project-specific files under `.ai/project`.
5. Generate AI entry files: `AGENTS.md`, `CLAUDE.md`, and `.kiro/steering`.
6. Create or link a GitHub Project from the organization template.
7. Create the initialization pull request.
8. Complete foundation issues before normal feature work starts.

## Validation

Run:

```bash
python scripts/validate-standard.py
```

The validation script checks the presence of required files and basic adapter consistency.
