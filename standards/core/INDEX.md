# Core Standard Index

Core standards are mandatory for every downstream project unless a rule is
explicitly marked overridable and the project records an approved exception.

## Documents

- `DEVELOPMENT.md`: implementation quality and change control
- `PROCESS.md`: lifecycle, phase gates, and method-independent process mapping
- `DEVELOPMENT_METHODS.md`: supported development methods and selection rules
- `NEXT_ACTION.md`: AI guidance flow for "what should I do next?"
- `AI_TOOL_COMPATIBILITY.md`: common behavior model across AI tools
- `REVIEW.md`: review types, required viewpoints, and approval rules
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

## Standard Development Model

Downstream projects may choose a method that fits their context. If no method
has been selected, use the adaptive default: small iterations, Kanban flow, and
W-model quality gates.

```text
Plan
  -> Requirements
  -> Design
  -> Implementation
  -> Developer verification
  -> Review
  -> Integration verification
  -> Release decision
  -> Retrospective and standard improvement
```

Each phase must define its expected input, output, review viewpoint, and test
viewpoint. The phase can be lightweight, but it must be explicit.

## AI Guidance

When a user asks "what should I do next?", AI tools must follow
`NEXT_ACTION.md`. They should inspect the project state, identify the current
phase, and recommend the safest next action. This is required so beginners can
use the project without already knowing GitHub Issues, PRs, or development
methods.

## Tool Compatibility

Codex, Claude Code, Kiro, and future AI tools must use the same task contract,
role names, quality viewpoints, and reporting shape. Tool-specific adapter
files are only entry points; they must not define conflicting standards.

## Project Adoption

The standard supports two downstream adoption paths:

- new project initialization from a template repository
- existing project adoption through a dedicated adoption issue and pull request

Both paths must install the same `.ai/managed` snapshot model. Existing project
adoption must preserve current files by default and defer enforcement until the
project can pass the required checks.
