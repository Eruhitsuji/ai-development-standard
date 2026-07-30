# New Project Flow

Use this flow when creating a new GitHub repository that should follow this standard.

## Inputs

Collect repository owner and name, visibility, selected standard version, selected profiles, enabled AI tools, maintainers, developer owners, runtime, package manager, and GitHub Project requirements.

## Flow

```text
Project request
  -> create repository from ai-project-template
  -> create initialization branch
  -> install standard snapshot into .ai/managed
  -> generate .ai/project files
  -> generate AGENTS.md, CLAUDE.md, and .kiro/steering
  -> add GitHub Issue and PR templates
  -> add validation workflow
  -> create initial foundation issues
  -> open initialization pull request
```

Normal feature development starts only after the initialization pull request is merged, project commands are defined, ownership rules exist, initial CI passes, and the first development Epic exists.
