# Quick Start

[日本語版](QUICKSTART.ja.md)

This guide provides a minimal local trial of the AI Development Standard. The
English documentation is authoritative. The Japanese Quick Start is a
convenience translation.

## Prerequisites

- Git
- Python 3.12 recommended
- a local clone of this repository
- an empty or disposable target directory

The current scripts use only the Python standard library.

## 1. Clone and validate the standard

```bash
git clone https://github.com/Eruhitsuji/ai-development-standard.git
cd ai-development-standard
python scripts/validate-standard.py
python scripts/run-standard-evals.py
python scripts/check-public-release.py
```

Or run the combined check:

```bash
./scripts/check.sh
```

On PowerShell:

```powershell
.\scripts\check.ps1
```

## 2. Record the exact standard commit

The installer copies files from the current checkout. Check out the intended
release or commit before installation, then record the same commit in the
project lock file.

Bash:

```bash
STANDARD_COMMIT="$(git rev-parse HEAD)"
```

PowerShell:

```powershell
$StandardCommit = git rev-parse HEAD
```

## 3. Install into a disposable project

Bash:

```bash
mkdir -p ../ai-standard-example
python scripts/init-project.py \
  --project-dir ../ai-standard-example \
  --mode new \
  --commit "$STANDARD_COMMIT" \
  --profiles core python \
  --install-github-templates
```

PowerShell:

```powershell
New-Item -ItemType Directory -Force ..\ai-standard-example | Out-Null
python scripts/init-project.py `
  --project-dir ..\ai-standard-example `
  --mode new `
  --commit $StandardCommit `
  --profiles core python `
  --install-github-templates
```

## 4. Inspect the generated project

The target directory should contain at least:

```text
.ai/
+-- standard.lock.yml
+-- managed/
+-- project/
AGENTS.md
CLAUDE.md
.kiro/steering/
.github/
```

Important ownership boundaries:

- `.ai/managed/**` is generated from the common standard and must not be edited
  during normal feature work.
- `.ai/project/**` contains project-specific rules, commands, roles, assurance,
  traceability, capabilities, permissions, and lifecycle settings.
- GitHub Issues remain the source of truth for actionable tasks.

## 5. Start with an AI assistant

Open the generated project with Codex, Claude Code, Kiro, or another compatible
assistant and ask one of these questions:

```text
What should I do next?
Review this project initialization and identify missing foundation work.
Turn this requirement into small GitHub Issues.
Check whether this proposed feature duplicates an existing capability.
Tell me only the decisions that require human approval.
```

The AI should read the project entry file, load the relevant standard sections
through `.ai/project/CONTEXT_INDEX.yml`, inspect available repository state, and
present a concise recommendation or decision request.

## 6. Try an existing-project adoption plan

Before changing an existing repository, generate a conservative plan:

```bash
python scripts/plan-adoption.py \
  --project-dir ../existing-project \
  --profiles core python
```

Then use a dedicated adoption Issue, branch, and pull request. Existing AI
instructions, CI, ownership files, and GitHub templates are preserved by
default and require explicit review before replacement.

## Current Limitations

This preview does not yet:

- execute evaluation scenarios against live AI models
- create GitHub Projects, labels, Rulesets, teams, or Merge Queue settings
  automatically
- fetch and verify a release artifact automatically
- verify that `--commit` matches the current local checkout
- provide a fully automated downstream standard-update pull request

See [Project Status](PROJECT_STATUS.md) for the current scope and stability
expectations.
