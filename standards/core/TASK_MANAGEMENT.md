# Task Management Standard

GitHub Issues are the source of truth for actionable work.

GitHub Projects are used for planning, prioritization, status, ownership, and
cross-project visibility.

## Status Values

```text
Inbox
Ready
Planned
In Progress
In Review
Blocked
Done
Cancelled
```

## Standard Fields

- Priority: P0, P1, P2, P3
- Size: XS, S, M, L, XL
- Executor Type: Human, AI, Human + AI
- AI Tool: None, Codex, Claude Code, Kiro, Multiple
- Role: Planner, Architect, Implementer, Reviewer, Tester, Integrator
- Write Scope
- Forbidden Scope
- Base Commit
- Parent Issue
- Blocked By
- Parallel Group
- Conflict Risk
- Review Agent
- Integration Owner
- Development Method
- Current Phase

## Issue Requirements

Implementation issues must include:

- purpose
- background
- scope
- out of scope
- acceptance criteria
- technical constraints
- verification method
- ownership
- write scope
- dependencies

Do not start implementation while an issue is `Inbox` or `Blocked`.

## Guidance Issues

Users may create guidance issues when they do not know what to do next.

Guidance issues are not implementation tasks. They should produce one of these
outputs:

- refined implementation issue
- investigation issue
- process decision issue
- foundation issue
- review or test plan
- recommendation to close as no action

Use `templates/github/ISSUE_TEMPLATE/guidance.yml` when the user needs help
choosing the next action.

## Process Decision Issues

Use process decision issues when a project, epic, or major task needs to select
or change its development method.

The decision must record:

- selected method
- quality gate model
- planning cadence
- release cadence
- reason for selection
- revisit condition

Use `templates/process-selection.md` for the decision body.

## Standard Adoption Issues

Existing project adoption must be tracked as a dedicated issue, not mixed into a
feature issue.

Adoption issues must include:

- target repository and default branch
- selected standard version and commit SHA
- adoption level: Passive, Guided, or Enforced
- selected profiles and enabled AI tools
- existing CI, issue templates, PR templates, CODEOWNERS, and AI instruction
  files
- files that must be preserved
- manual merge work for existing templates or instructions
- validation commands that can run now
- TODO items that require foundation follow-up issues

Adoption issue status should progress through:

```text
Inbox
  -> Ready
  -> In Progress
  -> In Review
  -> Done
```

Do not mark adoption `Done` until the adoption pull request is merged and
remaining foundation gaps are captured as separate issues.
