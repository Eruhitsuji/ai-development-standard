# Standard Evaluation Scenarios

These scenarios define expected AI behavior for common failure modes in
AI-assisted development. They are intentionally model-neutral.

`scripts/run-standard-evals.py` validates scenario structure now. Future
versions can execute the same scenarios against Codex, Claude Code, Kiro, or
other tools.

Each scenario must include:

- `scenario`
- `input`
- `expected.must`
- `expected.must_not`
- `applicable_rules`
- `assurance_level`
