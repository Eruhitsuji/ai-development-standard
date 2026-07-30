# Project-Specific Rules

This repository is the upstream source of the common standard.

Project-specific downstream rules must not be added to `standards/core`. Add reusable rules to a profile when they apply to a class of projects. Add one-off project rules to the downstream project's `.ai/project` directory.

Every change that affects downstream behavior must state:

- affected standard rule or template
- compatibility impact
- migration requirement
- versioning level: patch, minor, or major
