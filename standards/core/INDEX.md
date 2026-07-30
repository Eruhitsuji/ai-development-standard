# Core Standard Index

Core standards are mandatory for every downstream project unless a rule is explicitly marked overridable and the project records an approved exception.

## Documents

- `DEVELOPMENT.md`: implementation quality and change control
- `CODING.md`: coding conventions and maintainability
- `TESTING.md`: verification strategy and reporting
- `SECURITY.md`: secrets, input handling, and security review
- `GIT_GITHUB.md`: branch, pull request, and GitHub rules
- `TASK_MANAGEMENT.md`: Issues and Projects as the task source of truth
- `MULTI_AGENT_DEVELOPMENT.md`: multi-human and multi-AI parallel execution
- `STANDARD_DISTRIBUTION.md`: `.ai/managed` and `.ai/project` model
- `DEFINITION_OF_READY.md`: start conditions for AI-ready tasks
- `DEFINITION_OF_DONE.md`: completion conditions

## Non-Overridable Baseline

Downstream projects must not weaken these requirements:

- no secrets in repositories, prompts, logs, issues, or pull requests
- no direct push to protected default branches
- no implementation without a reviewable task source
- no final approval by the same AI that implemented the change
- no write-scope violations during parallel development
- no claim that checks passed unless they were executed
