# Project Status

## Current Stage

**Experimental Preview — intended for the v0.1.0 release.**

The project is suitable for evaluation, local trials, discussion, and early
adoption through reviewed pull requests. It is not yet a stable or fully
automated governance product.

## Implemented Scope

The repository currently provides:

- tool-neutral development standards for humans and AI agents
- Codex, Claude Code, and Kiro entry adapters
- GitHub Issue-driven task management
- small-task decomposition and complexity guidance
- requirement, capability, task, pull request, evidence, and release
  traceability
- specification change packages and artifact-consistency gates
- Quick, Standard, High, and Regulated assurance levels
- multi-human and multi-agent role separation
- review and merge governance, including stale-review rules
- lifecycle coverage from discovery through operations and retirement
- downstream templates for `.ai/managed` and `.ai/project`
- conservative new-project and existing-project installation helpers
- structural standard validation
- model-neutral evaluation scenario definitions

## Known Limitations

The v0.1.0 preview does not yet provide:

- live execution and scoring of evaluation scenarios against AI models
- automatic GitHub Project, label, Ruleset, team, or Merge Queue provisioning
- automatic download and cryptographic verification of release artifacts
- automatic confirmation that the installer `--commit` value matches the local
  checkout
- a complete downstream update planner and pull-request generator
- broad validation across many real production repositories
- a compatibility guarantee for pre-1.0 schemas and directory layouts

Some schema files currently describe lightweight contracts rather than complete
JSON Schema validation. Some governance controls are documented and templated
but still depend on repository settings and human review for enforcement.

## Stability Policy Before 1.0

Until version 1.0:

- minor releases may add or reorganize standards and templates
- breaking changes may occur when the migration path is documented
- downstream projects should pin both the release version and commit SHA
- standard updates should be reviewed in dedicated pull requests
- production use should start with a pilot repository and explicit exceptions
  where needed

## Language Policy

English is the authoritative language for the repository, standards, schemas,
templates, scripts, Issues, pull requests, and release notes.

`docs/QUICKSTART.ja.md` is provided as a convenience translation. If the English
and Japanese Quick Starts differ, the English version is authoritative.

## Intended Use

This project is intended as a governance and coordination layer. It may be used
alongside specification-driven development tools, agent frameworks, task
planners, CI systems, and repository automation.

It is not intended to:

- replace human accountability for requirements, merge, release, deployment,
  destructive operations, or risk acceptance
- make every change follow the same process weight
- replace GitHub Issues with a second task database
- guarantee that an AI model will follow the standard without evaluation and
  enforcement

## Feedback Priorities

Early feedback is especially useful for:

- whether AI tools load the correct standards at the correct time
- whether Issue templates produce sufficiently small and unambiguous tasks
- whether assurance levels are practical
- whether review and merge rules are enforceable for individual and team use
- whether installation preserves existing repository conventions
- whether the standard creates excessive context or documentation overhead
