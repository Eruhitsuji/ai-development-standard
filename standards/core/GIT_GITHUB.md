# Git and GitHub Standard

Default branch: `main`.

Recommended branch names:

```text
feature/<issue>-short-name
fix/<issue>-short-name
task/<issue>-short-name
docs/<issue>-short-name
ai/codex/<issue>-short-name
ai/claude/<issue>-short-name
ai/kiro/<issue>-short-name
chore/standard-update-v<version>
```

Every pull request must include related issue, purpose, changes, out-of-scope items, verification results, security impact, compatibility impact, AI involvement, and remaining risks.

Protect `main` with pull requests, required checks, code owner review where available, stale approval dismissal, unresolved conversation blocking, disabled force push, disabled branch deletion, and merge queue when useful.
