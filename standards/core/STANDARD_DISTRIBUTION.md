# Standard Distribution Standard

The common standard is distributed to downstream projects as a committed, version-locked snapshot.

```text
.ai/
├── standard.lock.yml
├── managed/
└── project/
```

`.ai/managed/**` is owned by the common standard and is not edited during feature work. `.ai/project/**` is owned by the downstream project. `AGENTS.md`, `CLAUDE.md`, and `.kiro/steering/**` are generated adapter entry files and should be changed by the integrator or standard update task.

Every downstream project must record standard repository, version, commit SHA, installed profiles, adapter versions, and install/update timestamp. Do not use floating branches such as `main` for required standards.
