# Standard Distribution Standard

The common standard is distributed to downstream projects as a committed,
version-locked snapshot.

## Downstream Directories

```text
.ai/
+-- standard.lock.yml
+-- managed/
+-- project/
```

## Adoption Modes

The same downstream layout is used for new and existing projects.

New projects install the standard during repository initialization. Existing
projects install it through a dedicated adoption pull request.

| Mode | Managed Snapshot | Project Rules | Existing Files |
| --- | --- | --- | --- |
| New project | created during bootstrap | generated from templates | minimal or absent |
| Existing project | added or refreshed in adoption PR | created with TODOs where needed | preserved by default |

Existing project adoption must not rewrite or delete established CI, templates,
AI instructions, branch rules, or ownership files unless the adoption pull
request explicitly documents the change and rollback path.

## Ownership

| Path | Owner | Normal feature edits |
| --- | --- | --- |
| `.ai/managed/**` | common standard | prohibited |
| `.ai/project/**` | downstream project | allowed |
| `.ai/standard.lock.yml` | standard update process | prohibited outside update tasks |
| `AGENTS.md` | generated adapter plus project entry | integrator only |
| `CLAUDE.md` | generated adapter plus project entry | integrator only |
| `.kiro/steering/**` | generated adapter plus project entry | integrator only |

## Lock File

Every downstream project must record:

- standard repository
- version
- commit SHA
- installed profiles
- adapter versions
- install/update timestamp

Do not use floating branches such as `main` for required standards.

## Existing Project Adoption

When installing the standard into an existing project:

- create an adoption issue first
- audit existing workflows, templates, commands, owners, and AI instruction files
- create a dedicated adoption branch
- install `.ai/managed/**` and `.ai/standard.lock.yml`
- create missing `.ai/project/**` files without inventing unknown commands
- preserve existing `AGENTS.md`, `CLAUDE.md`, `.kiro/`, and `.github/` files by
  default
- record preserved files and manual merge work in the adoption pull request
- defer branch-rule enforcement until required checks are stable

The project may start at a passive or guided adoption level and move to enforced
operation later.
