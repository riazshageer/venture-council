# Contributing to Venture Council

Thank you for improving Boardroom and its specialist council.

## Development setup

1. Fork the repository and clone your fork.
2. Add the upstream repository:

   ```bash
   git remote add upstream git@github.com:riazshageer/venture-council.git
   ```

3. Verify the checkout:

   ```bash
   python3 scripts/validate_boardroom.py
   python3 -m unittest discover -s tests -v
   ```

Python 3.10 or later is required. No third-party Python packages are needed.

## Feature-branch workflow

Never commit directly to `main`. Begin each change from an up-to-date `main`:

```bash
git switch main
git pull --ff-only upstream main
git switch -c feat/short-purpose
```

Use a short branch name with one of these prefixes:

- `feat/` for new behavior.
- `fix/` for bug fixes.
- `docs/` for documentation only.
- `refactor/` for behavior-preserving restructuring.
- `test/` for test-only changes.
- `chore/` for maintenance.
- `release/` for release preparation.

Keep one concern per branch where practical. If a change becomes broad, split independent work into separate branches and pull requests.

## Commits

Use Conventional Commits:

```text
type(scope): imperative summary
```

Examples:

```text
feat(installer): add managed Windows copies
fix(memory): preserve learned playbooks during upgrades
docs(readme): explain conflict recovery
```

Keep commits atomic. Stage only the files or hunks that belong to one concern and review `git diff --staged` before committing.

## Before opening a pull request

Run:

```bash
python3 scripts/validate_boardroom.py
python3 -m unittest discover -s tests -v
sh -n install.sh                 # Linux and macOS
```

When changing a skill, also validate it with the skill validator available in your agent environment. When changing installers, test both ordinary uninstall and preservation of global learned knowledge.

Update your branch without creating an unnecessary merge commit:

```bash
git fetch upstream
git rebase upstream/main
```

Force-push only your own feature branch and use `--force-with-lease`.

## Pull requests

Push the branch to your fork and open a pull request into `main`. Complete the pull-request template, keep CI green, resolve review conversations, and use squash merge unless preserving distinct atomic commits materially improves history.

Pull requests require review and the repository's `Quality gate` check. Direct pushes and force pushes to `main` are blocked.

## Council knowledge contributions

Employees and playbooks require more than plausible prose. Include authoritative source IDs, freshness metadata, professional boundaries, and evidence that the addition fills a genuine gap. Never contribute client-confidential or repository-specific information to global council knowledge.

## Reporting security issues

Do not open a public issue for a vulnerability that could expose credentials, private data, or unsafe execution. Contact the repository owner privately through GitHub until a dedicated security policy and reporting channel are published.
