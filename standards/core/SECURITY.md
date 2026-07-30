# Security Standard

## Non-Overridable Rules

- Do not commit credentials, API keys, tokens, private keys, or session cookies.
- Do not paste secrets into AI prompts, issues, pull requests, logs, or tests.
- Do not weaken authentication, authorization, input validation, or audit logs without explicit approval.
- Do not disable security checks to make CI pass.

Validate untrusted input before using it in database queries, shell commands, file paths, URLs, templates, or deserialization. Prefer structured APIs over string-built commands or queries.

Request focused security review for authentication, authorization, secrets handling, dependency installation, network access, file transfer, encryption, signing, or GitHub Actions permissions.
