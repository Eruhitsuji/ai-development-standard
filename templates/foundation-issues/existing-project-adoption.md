# Existing Project Adoption Foundation Epic

## Purpose

Adopt the AI development standard in an existing repository without disrupting
current development or release work.

## Scope

- install the standard snapshot
- preserve existing project behavior and workflows
- add or align AI entry files
- add project-specific standard files
- identify follow-up work needed before enforcement

## Foundation Tasks

- [ ] Inventory existing languages, runtimes, package managers, and frameworks
- [ ] Inventory existing CI, branch rules, issue templates, PR templates, and CODEOWNERS
- [ ] Inventory existing `AGENTS.md`, `CLAUDE.md`, and `.kiro/steering/**`
- [ ] Install `.ai/managed/**` and `.ai/standard.lock.yml`
- [ ] Create `.ai/project/PROJECT.yml`, `COMMANDS.yml`, `OWNERS.yml`, `SCOPES.yml`, and `EXCEPTIONS.yml`
- [ ] Add standard references to existing AI entry files without deleting project-specific rules
- [ ] Add or merge issue and pull request template sections
- [ ] Add standard validation workflow without replacing existing CI
- [ ] Create follow-up issues for TODO commands, ownership gaps, or branch-rule enforcement
- [ ] Decide activation level: Passive, Guided, or Enforced

## Acceptance Criteria

- [ ] adoption pull request is merged
- [ ] existing CI and project behavior are preserved
- [ ] `.ai/adoption/REPORT.md` lists preserved files and manual review items
- [ ] enabled AI tools can find `.ai/managed` and `.ai/project`
- [ ] standard validation succeeds
- [ ] stricter enforcement is deferred or explicitly approved

## Verification

```text
python scripts/validate-standard.py
existing project checks that are already reliable
```
