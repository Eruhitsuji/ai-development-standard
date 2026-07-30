# Normal Development Flow

Normal development is GitHub Issue driven.

```text
1 Issue = 1 executor = 1 branch/worktree = 1 pull request
```

1. Create or select a GitHub Issue.
2. Confirm the issue satisfies the Definition of Ready.
3. Assign executor, owner, reviewer, and integration owner.
4. Define write scope, forbidden scope, dependencies, and acceptance criteria.
5. Create a dedicated branch or worktree.
6. Implement only within the assigned scope.
7. Run required verification commands.
8. Open a pull request linked to the issue.
9. Review through another AI and a human/code owner when required.
10. Merge through CI and merge queue.
11. Close the issue and remove the worktree.
