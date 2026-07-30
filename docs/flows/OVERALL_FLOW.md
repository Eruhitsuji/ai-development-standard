# Overall Flow

This standard coordinates four connected workflows:

1. creating a new project
2. adopting the standard in an existing project
3. executing normal development
4. updating the common standard

## System Overview

```text
GitHub account or organization
|
+-- ai-development-standard
|   +-- common standards
|   +-- profiles
|   +-- AI adapters
|   +-- bootstrap/update scripts
|
+-- ai-project-template
|   +-- minimal new repository template
|
+-- existing downstream project
|   +-- adoption issue
|   +-- adoption branch
|   +-- adoption pull request
|
+-- downstream project
    +-- .ai/managed      fixed standard snapshot
    +-- .ai/project      project-specific rules
    +-- AGENTS.md        Codex entry
    +-- CLAUDE.md        Claude Code entry
    +-- .kiro/steering   Kiro entry
    +-- GitHub Issues    task contracts
    +-- pull requests    integration units
```

## Operating Principle

```text
GitHub Issue
  -> branch or worktree
  -> implementation and verification
  -> pull request
  -> independent review
  -> CI and merge queue
  -> main
```

Human developers and AI tools use the same task and isolation model. The
difference is responsibility: humans own requirements, approval, and final
judgment; AI tools assist with planning, implementation, verification, and
first-pass review.

## Adoption Paths

New repositories use `docs/flows/NEW_PROJECT.md`.

Existing repositories use `docs/flows/EXISTING_PROJECT_ADOPTION.md`. Existing
adoption is deliberately staged: preserve current workflows first, then add
standard entry files, validation, templates, ownership, and enforcement through
reviewed pull requests.
