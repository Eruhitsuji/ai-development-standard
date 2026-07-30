# Standard Update Flow

## Upstream Change

1. Create a standard change issue.
2. Implement the standard change in this repository.
3. Update affected docs, profiles, adapters, schemas, templates, and scripts.
4. Decide version level: patch, minor, or major.
5. Run standard validation.
6. Merge after review.
7. Create a release tag.

## Downstream Adoption

Each downstream project receives a separate update pull request.

```text
standard v0.1.0
  -> downstream update branch
  -> .ai/managed update
  -> .ai/standard.lock.yml update
  -> adapter regeneration
  -> project-specific conflict check
  -> project owner review
  -> merge
```

Do not update downstream projects by reading a local untracked standard. Do not apply major updates automatically.
