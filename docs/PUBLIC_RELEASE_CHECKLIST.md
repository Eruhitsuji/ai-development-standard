# Public Release Checklist

Use this checklist before changing repository visibility to public and before
creating a release tag.

## 1. Legal and Public Documentation

- [ ] `LICENSE` contains the intended MIT License text and copyright holder.
- [ ] `SECURITY.md` explains private vulnerability reporting.
- [ ] `docs/QUICKSTART.md` completes successfully from a clean checkout.
- [ ] `docs/QUICKSTART.ja.md` is consistent with the authoritative English guide.
- [ ] `docs/PROJECT_STATUS.md` accurately states implemented and missing features.
- [ ] README links to the license, security policy, Quick Starts, status, and this
      checklist.

## 2. Repository Validation

Run from a clean checkout of the exact release candidate commit:

```bash
python scripts/validate-standard.py
python scripts/run-standard-evals.py
python scripts/check-public-release.py
git diff --check
```

Or:

```bash
./scripts/check.sh
```

On PowerShell:

```powershell
.\scripts\check.ps1
```

Record command results in the release pull request.

## 3. Installation Smoke Tests

Test both supported adoption modes in disposable directories.

### New project

```bash
STANDARD_COMMIT="$(git rev-parse HEAD)"
python scripts/init-project.py \
  --project-dir ../public-release-new-project \
  --mode new \
  --commit "$STANDARD_COMMIT" \
  --profiles core python \
  --install-github-templates
```

Confirm:

- [ ] `.ai/standard.lock.yml` records the intended repository, version, and SHA.
- [ ] `.ai/managed/**` contains the expected core and profile snapshot.
- [ ] `.ai/project/**` contains required project templates.
- [ ] `AGENTS.md`, `CLAUDE.md`, and `.kiro/steering/**` reference existing files.
- [ ] GitHub Issue and pull request templates are installed when requested.

### Existing project

- [ ] Run `scripts/plan-adoption.py` against a representative existing project.
- [ ] Run `scripts/init-project.py --mode existing` on a disposable copy.
- [ ] Confirm existing AI instructions, CI, ownership, and templates are not
      overwritten silently.
- [ ] Review `.ai/adoption/REPORT.md`.

## 4. Sensitive Information Review

The repository script checks current tracked text files for a small set of
high-confidence secret patterns. It does not prove that the repository history
is clean.

Review all of the following before publication:

- [ ] current tracked files
- [ ] deleted and renamed files in Git history
- [ ] commit messages
- [ ] Issues and pull requests that will become public
- [ ] review comments and attachments
- [ ] GitHub Actions logs and downloadable artifacts
- [ ] local paths, internal hostnames, private URLs, email addresses, and personal
      information

Recommended history scanners include Gitleaks or TruffleHog. Example commands:

```bash
gitleaks git . --redact
trufflehog git file://. --only-verified
```

These tools are optional external dependencies and are not installed by this
repository.

If any secret was committed:

1. revoke or rotate it first
2. remove it from the repository and relevant logs or artifacts
3. rewrite history when necessary
4. re-run scans
5. assume existing clones or forks may retain the secret

## 5. GitHub Public Settings

Before changing visibility:

- [ ] repository description clearly says experimental, tool-neutral, and
      GitHub-focused
- [ ] topics are configured, for example `ai-development`, `github`,
      `multi-agent`, `governance`, and `specification`
- [ ] Issues are enabled
- [ ] private vulnerability reporting is enabled when available
- [ ] default branch is `main`
- [ ] direct pushes and force pushes are prohibited where supported
- [ ] required validation checks are configured
- [ ] stale approvals are dismissed after new pushes where supported
- [ ] repository secrets and environment secrets contain no obsolete values
- [ ] Actions permissions follow least privilege

## 6. Release Preparation

- [ ] release PR is reviewed against the latest head commit
- [ ] implementing AI is not the final approver
- [ ] release authority is human
- [ ] `VERSION` is `0.1.0`
- [ ] `CHANGELOG.md` represents the release contents
- [ ] release notes describe the project as an Experimental Preview
- [ ] known limitations are copied or linked from `docs/PROJECT_STATUS.md`
- [ ] rollback plan is to restore private visibility or publish a corrective
      release if a serious disclosure or packaging issue is found

Recommended release title:

```text
v0.1.0 — Initial Experimental Preview
```

## 7. Publication Order

1. Merge the reviewed public-release preparation PR.
2. Run the checklist on the merged `main` commit.
3. Change repository visibility to public.
4. Confirm public pages, links, workflows, Issues, and security settings.
5. Create annotated tag `v0.1.0` from the reviewed commit.
6. Create the GitHub Release using the approved release notes.
7. Repeat the Quick Start using the public clone URL.

## 8. Post-Release Verification

- [ ] public clone works without authentication
- [ ] license is detected by GitHub
- [ ] security reporting instructions are visible
- [ ] English and Japanese Quick Starts render correctly
- [ ] validation workflow succeeds on `main`
- [ ] release archive contains the expected files
- [ ] no private Issues, pull-request text, logs, or artifacts were exposed
      unexpectedly
- [ ] initial feedback is captured as GitHub Issues rather than untracked notes
