# Testing Standard

Behavioral changes require tests unless an approved exception explains why.

Bug fixes should include a regression test whenever practical.

## Test Levels

- unit tests: isolated behavior of functions, classes, and modules
- integration tests: contracts between components or external adapters
- end-to-end tests: user-visible workflows and deployment-critical paths

Pull requests must report commands executed, pass/fail result, tests not run, reason tests were not run, and residual risk. Never mark an unchecked item as complete.
