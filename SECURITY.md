# Security Policy

## Supported Versions

This project is currently an experimental preview. Security fixes are applied to
the latest released version and the current `main` branch. Older pre-1.0
versions may not receive backports.

## Reporting a Vulnerability

Do not disclose vulnerabilities, credentials, private repository information,
or exploit details in a public Issue, Discussion, pull request, or commit.

Preferred reporting method:

1. Open the repository's **Security** tab.
2. Select **Report a vulnerability** if private vulnerability reporting is
   enabled.
3. Include the affected version or commit, impact, reproduction steps, and any
   suggested mitigation.

If private vulnerability reporting is unavailable, open a minimal public Issue
named `Security contact request` without technical details or secrets. Ask the
maintainer to establish a private communication channel before sharing the
report.

## What to Include

A useful report contains:

- affected release, commit, file, workflow, or template
- expected and observed behavior
- security impact and likely attack conditions
- minimal reproduction steps
- whether credentials, personal data, or destructive actions are involved
- suggested mitigation when known

## Coordinated Disclosure

Please allow the maintainer time to investigate and prepare a fix before public
disclosure. Response and remediation are best effort; this experimental project
does not currently guarantee a service-level agreement.

## Secrets and Sensitive Data

Never include real API keys, tokens, passwords, private keys, internal URLs,
personal data, or production configuration in examples, evaluation scenarios,
Issue bodies, pull requests, logs, or generated downstream templates.

If a secret is committed, revoke or rotate it first. Removing it from the latest
commit is not sufficient because it may remain in Git history, forks, caches,
workflow logs, or downloaded artifacts.
