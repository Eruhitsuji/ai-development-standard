# Project Foundation Epic

## Purpose

Prepare a new repository for normal development under the AI development
standard.

## Scope

- confirm product and project ownership
- define architecture and directory structure
- define project commands
- add initial CI
- configure issue and pull request templates
- configure ownership and review rules
- create the first development Epic

## Foundation Tasks

- [ ] Confirm product purpose and users in `.ai/project/PRODUCT.md`
- [ ] Confirm project owner and technical owners in `.ai/project/OWNERS.yml`
- [ ] Define setup, format, lint, test, and full-check commands in `.ai/project/COMMANDS.yml`
- [ ] Document initial architecture in `.ai/project/ARCHITECTURE.md`
- [ ] Document repository structure in `.ai/project/STRUCTURE.md`
- [ ] Confirm scope rules in `.ai/project/SCOPES.yml`
- [ ] Add or confirm CI for the standard validation and project checks
- [ ] Add issue and pull request templates
- [ ] Add CODEOWNERS or equivalent ownership rules
- [ ] Create the first development Epic with acceptance criteria

## Acceptance Criteria

- [ ] `.ai/standard.lock.yml` records the selected standard version and commit
- [ ] `.ai/project/**` has no unexplained TODOs for required startup work
- [ ] AI entry files exist for enabled tools
- [ ] at least one validation command succeeds
- [ ] remaining gaps are represented as issues

## Verification

```text
python scripts/validate-standard.py
project-specific checks from .ai/project/COMMANDS.yml
```
