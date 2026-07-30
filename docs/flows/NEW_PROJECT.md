# New Project Flow

Use this flow when creating a new GitHub repository that should follow this
standard.

Do not use this flow to retrofit a repository that already has code, history,
CI, issue templates, or project-specific conventions. Use
`docs/flows/EXISTING_PROJECT_ADOPTION.md` for that case.

## Inputs

Create or collect a project request with:

- repository owner and name
- visibility
- selected standard version
- selected profiles
- enabled AI tools
- maintainer and developer owners
- expected runtime and package manager
- whether GitHub Project setup is required

The canonical template is `templates/project-request.yml`.

Use `templates/foundation-issues/new-project.md` as the starter body for the
project foundation Epic.

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

## Development Start Gate

Normal feature development starts only after:

- the initialization pull request is merged
- `PROJECT.yml` has a project owner
- `COMMANDS.yml` has real setup/check commands or explicit exceptions
- CODEOWNERS or equivalent ownership rules exist
- initial CI passes
- the first development Epic exists

## Generated Downstream Layout

```text
project/
+-- .ai/
|   +-- standard.lock.yml
|   +-- managed/
|   +-- project/
+-- AGENTS.md
+-- CLAUDE.md
+-- .kiro/steering/
+-- .github/
```
