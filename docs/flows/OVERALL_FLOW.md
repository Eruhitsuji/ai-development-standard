# Overall Flow

This standard coordinates three connected workflows: creating a new project, executing normal development, and updating the common standard.

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
+-- downstream project
    +-- .ai/managed      fixed standard snapshot
    +-- .ai/project      project-specific rules
    +-- AGENTS.md        Codex entry
    +-- CLAUDE.md        Claude Code entry
    +-- .kiro/steering   Kiro entry
    +-- GitHub Issues    task contracts
    +-- pull requests    integration units
```

Human developers and AI tools use the same task and isolation model. Humans own requirements, approval, and final judgment; AI tools assist with planning, implementation, verification, and first-pass review.
