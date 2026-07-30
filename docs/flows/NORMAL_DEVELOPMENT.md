# Normal Development Flow

Normal development is GitHub Issue driven.

## Unit of Work

```text
1 Issue = 1 executor = 1 branch/worktree = 1 pull request
```

The executor can be a human, Codex, Claude Code, Kiro, or a human working with
an AI assistant.

## Flow

1. Create or select a GitHub Issue.
2. Confirm the issue satisfies the Definition of Ready.
3. Identify the selected development method and lifecycle phase.
4. Assign executor, owner, reviewer, and integration owner.
5. Define write scope, forbidden scope, dependencies, and acceptance criteria.
6. Create a dedicated branch or worktree.
7. Implement only within the assigned scope.
8. Run required verification commands.
9. Open a pull request linked to the issue.
10. Review through another AI and a human/code owner when required.
11. Merge through CI and merge queue.
12. Close the issue and remove the worktree.

If the next step is unclear, use `standards/core/NEXT_ACTION.md` before
continuing. The correct output may be a refined issue or investigation rather
than code.

## Parallel Work

Tasks may run in parallel only when:

- dependencies do not block each other
- write scopes do not overlap
- shared contracts are stable
- shared files have a named integrator
- each task has an independent pull request
