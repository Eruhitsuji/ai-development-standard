# Development Standard

## Principles

- Prefer small, reviewable changes.
- Preserve compatibility unless an approved issue authorizes a breaking change.
- Follow existing project architecture before adding new abstractions.
- Add abstractions only when they remove real duplication or clarify ownership.
- Treat documentation and tests as part of the deliverable.

## Change Control

Every non-trivial change must be linked to a GitHub Issue, acceptance criteria, verification commands, and a pull request.

Out-of-scope work discovered during implementation must be recorded as a new issue rather than silently added to the current pull request.

## Dependencies

Add dependencies only when the problem is not better solved by existing project code, the dependency is maintained, license/security posture is acceptable, and verification is updated.
