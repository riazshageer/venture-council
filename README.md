# Boardroom

Boardroom is a globally installed AI business-consulting council for OpenAI Codex and Claude Code. A user-facing Team Lead turns an unclear idea into a structured brief, selects only the specialists needed, coordinates direct work, consultations, councils, or parallel programs, and returns one integrated plan.

Boardroom is designed for progressive discovery. The runtime sees a short skill description first, then the Team Lead instructions, then council/playbook indexes, and only then the employee profiles or playbooks required for the engagement. It does not load a dozen personas into every conversation.

## What it includes

- A Team Lead workflow for discovery, staffing, orchestration, cost-quality routing, reconciliation, and delivery.
- Twelve specialist profiles covering brand, perception, UX, design, financial planning, cloud, software architecture, software engineering, business, marketing, social media, and AI automation.
- Initial Angular, NestJS, Rust, CSS, semantic HTML, Facebook/Instagram, LinkedIn, TikTok, and YouTube playbooks.
- Durable engagement memory separated into briefs, questions, assumptions, plans, decisions, reports, research, deliverables, and retrospectives.
- Evidence, freshness, governance, approval, and quality protocols.
- A controlled workflow for researching and promoting new employees or playbooks.
- Thin Codex and Claude Code adapters over one provider-neutral core.
- A writable global knowledge home that remains independent of every client repository.
- Upgrade-safe preservation and auditing of learned employees and playbooks.
- Deterministic validation and packaging scripts.

## How Boardroom works

Boardroom chooses the smallest sufficient execution shape:

| Shape | Use |
|---|---|
| Direct | Narrow, low-risk work the Team Lead can handle from broad knowledge |
| Consult | One or two focused specialist questions |
| Council | Several interacting disciplines that need reconciliation |
| Program | Complex/high-impact work requiring bounded parallel workstreams or subcommittees |

Employees are not fictional executives whose opinions are generated for entertainment. Each receives a bounded question, relevant context, an expected artifact, evidence requirements, and a stopping condition. The Team Lead resolves conflicts against the user's goals and records material dissent.

## Requirements

- Python 3.10 or later.
- At least one of OpenAI Codex or Claude Code installed and available on `PATH`.
- Windows 10/11, macOS, or Linux.
- Internet/research tooling for time-sensitive work. Boardroom can operate without it, but must label unsupported assumptions and cannot responsibly make current platform, price, legal, or market claims.
- Optional MCP servers or connectors for data and actions relevant to an engagement.

Boardroom contains no runtime dependency and requires no API key by itself.

Check a downloaded copy before installation:

```bash
python3 scripts/check_prereqs.py --provider all
```

On Windows PowerShell, use `python` or `py -3` in place of `python3` when appropriate.

## Quick install from the latest GitHub release

No repository clone is required. On Linux or macOS:

```bash
curl -fsSL https://raw.githubusercontent.com/riazshageer/venture-council/main/install.sh | sh
```

Install for only one provider by downloading the script before running it:

```bash
curl -fsSLO https://raw.githubusercontent.com/riazshageer/venture-council/main/install.sh
sh install.sh codex   # or: sh install.sh claude
```

On Windows PowerShell:

```powershell
irm https://raw.githubusercontent.com/riazshageer/venture-council/main/install.ps1 -OutFile install.ps1
.\install.ps1 -Provider all
```

Review remote scripts before running them when required by your security practices. Both scripts download the immutable archives attached to the latest GitHub Release and run the same Python installer described below.

If this repository is published under a different owner or name, set `BOARDROOM_GITHUB_REPOSITORY` to `owner/repository` before running the downloaded script, or pass `-Repository owner/repository` to `install.ps1`.

## Install from a clone or downloaded archive

Clone, copy, or extract the distribution, then run:

```bash
python3 scripts/install_global.py --provider all
```

Use `--provider codex` or `--provider claude` to install for only one agent.

The default global application home is:

```text
${XDG_DATA_HOME}/boardroom     # when XDG_DATA_HOME is set
~/.local/share/boardroom       # otherwise
%LOCALAPPDATA%\Boardroom       # Windows
```

Set `BOARDROOM_HOME` before installation and use to choose a different location. The installer places replaceable runtime files under `app/`, writable shared knowledge under `core/`, the previous bundled baseline under `bundled-core/`, conflicts under `conflicts/`, and knowledge-change history under `audit/`.

It registers global skills at `${CODEX_HOME}/skills` or `~/.codex/skills` for Codex and `~/.claude/skills` for Claude Code. Claude's optional researcher and critic agents are registered under `~/.claude/agents`. Unix installations use managed symbolic links. Windows installations use managed copies so Developer Mode and administrator symlink privileges are not required.

After installation, Boardroom is available from any repository. Ask naturally:

```text
I have an idea for a service that helps independent Caribbean restaurants
predict ingredient demand. Help me determine whether it is a viable business.
```

Or invoke the skill explicitly where supported:

```text
Use the boardroom skill to turn this idea into a validation plan.
```

The agent should begin with focused discovery. It should not convene the full council by default. Check the installation at any time with:

```bash
python3 scripts/boardroom_home.py check
```

If the installer reports an existing unmanaged path, inspect it first. `--force` backs that path up with a timestamp before installing Boardroom; it does not silently delete it.

## Uninstall

Remove Boardroom from both agents while preserving global knowledge, audit history, backups, and conflict files:

```bash
python3 scripts/uninstall_global.py --provider all
```

Use `--provider codex` or `--provider claude` to unregister only one agent. The uninstaller removes only symlinks or copies it can verify are Boardroom-managed.

To permanently delete the entire global Boardroom home as well:

```bash
python3 scripts/uninstall_global.py --provider all --purge
```

The command prompts before deletion. For intentional non-interactive removal, add `--yes`. Purging deletes learned employees, playbooks, audit history, backups, and unresolved upgrade conflicts and cannot be undone unless you have a backup.

## Package for Codex

Build a self-contained Codex plugin directory:

```bash
python3 scripts/package_boardroom.py codex dist/boardroom-codex
```

The package contains a complete installable distribution:

```text
dist/boardroom-codex/
├── .codex-plugin/plugin.json
├── AGENTS.md
├── adapters/
├── capability-tiers.md
├── core/
├── scripts/
└── skills/
```

After extracting or entering the generated directory, run `python3 scripts/install_global.py --provider codex`. Loading the manifest alone packages the skill but does not initialize its writable global knowledge home.

Boardroom intentionally does not hardcode model names. The Codex adapter maps `economy`, `standard`, `deep`, `research`, and `critic` intentions to models and tools currently available to the user. Verify current model availability and pricing through official OpenAI documentation before implementing programmatic routing.

## Package for Claude Code

Build a self-contained Claude Code plugin directory:

```bash
python3 scripts/package_boardroom.py claude dist/boardroom-claude
```

The package contains:

```text
dist/boardroom-claude/
├── .claude-plugin/plugin.json
├── CLAUDE.md
├── adapters/
├── agents/
├── capability-tiers.md
├── core/
├── scripts/
└── skills/
```

After extracting or entering the generated directory, run `python3 scripts/install_global.py --provider claude`. The installation adds optional isolated research and critic subagents; the Team Lead still owns staffing and synthesis.

## Global knowledge and repository memory

Boardroom keeps reusable capability globally:

```text
<boardroom-home>/
├── app/                # replaceable runtime and installed skill sources
├── core/               # writable global council, playbooks and protocols
├── bundled-core/       # baseline used for upgrade-safe merging
├── conflicts/          # new upstream versions that conflict with learned edits
├── audit/              # append-only knowledge-change records
└── installation.json
```

New employees, playbooks, and improvements to Boardroom itself are written only to this global `core/`. They must never be stored in the repository currently being consulted.

Repository-specific facts and decisions remain with that repository. Before creating Boardroom's default state, the Team Lead inspects repository instructions and existing memory conventions. If the repository clearly defines its own memory system and writing is in scope, Boardroom uses it. Otherwise it creates:

For work that should persist, Boardroom creates:

```text
.boardroom/engagements/<slug>/
├── brief.md
├── open-questions.md
├── assumptions.md
├── plan.md
├── decisions.md
├── retrospective.md
├── research/       # only when needed
├── reports/        # only when needed
└── deliverables/   # only when needed
```

The templates come from the global Boardroom core. Project memory contains only engagement information. It must not contain reusable Boardroom employee or playbook files.

Do not store API keys, passwords, personal identifiers, or unnecessary confidential data in engagement memory.

## Example prompts

Small request:

```text
Help me sharpen the value proposition for a one-person bookkeeping service.
Keep this lightweight and tell me what assumptions you make.
```

Medium consultation:

```text
Use Boardroom to design a validation plan and basic unit economics for a
subscription meal-prep idea in Trinidad and Tobago. I can spend TT$5,000 on tests.
```

Complex program:

```text
Use Boardroom to prepare this validated B2B prototype for launch. I need positioning,
critical UX journeys, a financial scenario model, target architecture, cloud options,
an AI automation plan, and a measured go-to-market roadmap. Stop for approval before
any external action or permanent council change.
```

Current social strategy:

```text
Assess which social platforms are viable for this business in my market. Refresh any
expired platform playbooks from official sources before relying on platform mechanics.
```

## Adding an employee or playbook

Use the `create-boardroom-employee` skill only after the global council and playbook indexes demonstrate a real gap.

The lifecycle is:

1. Define the missing decisions and outputs.
2. Prefer a playbook owned by an existing specialist when the gap is technology-, platform-, domain-, or jurisdiction-specific.
3. Research authoritative current sources.
4. Create a `candidate` artifact with provenance and freshness metadata.
5. Test it against overlap, safety, links, metadata, and a realistic scenario.
6. Promote it to `active` in the global home, update the global index, validate it, and append an audit record.

Employee files put duties and skills first. Required metadata is documented in `core/schemas/knowledge-artifact.md`.

Never promote client names, confidential facts, proprietary data, or repository-specific decisions. Generalize the capability and preserve only the evidence needed to support it.

## Upgrade behavior

Run the global installer again from a newer Boardroom distribution to upgrade:

```bash
python3 scripts/install_global.py --provider all
```

The installer compares the new bundled core, the previous bundled baseline, and the live learned core:

- Untouched bundled files update automatically.
- New bundled files are added.
- Learned files are preserved.
- When both the bundled file and learned file changed, the learned version remains active and the new bundled version is written under `conflicts/<timestamp>/` for review.
- Runtime files under `app/` are replaced and provider links continue to point at them.

### Resolve an upgrade conflict

For a conflict, the active learned file remains under `<boardroom-home>/core/` and the incoming bundled version is written under `<boardroom-home>/conflicts/<timestamp>/` with the same relative path.

1. Back up the global home.
2. Compare the active learned file, the incoming conflict file, and the previous bundled baseline under `bundled-core/`.
3. Merge the useful upstream changes into the active file without removing validated learned knowledge.
4. Update artifact version, review date, sources, and index metadata when applicable.
5. Run global validation:

   ```bash
   python3 /path/to/boardroom-home/app/scripts/validate_boardroom.py --core /path/to/boardroom-home/core
   ```

6. Remove the resolved conflict copy only after validation and review.

Do not replace the whole live `core/` with `bundled-core/`; that would discard learned knowledge.

### Back up and recover

Boardroom's complete durable state is the global application home. Back up that directory before upgrades or major knowledge changes.

To recover while preserving learned knowledge:

1. Restore the backed-up `core/` and `audit/` directories into the chosen Boardroom home.
2. Run the installer from the desired release. It restores runtime files and provider registrations while merging bundled knowledge against the restored core.
3. Run `boardroom_home.py check` and global validation.
4. Restart Codex or Claude Code sessions so skill discovery refreshes.

If only runtime files are damaged, rerun the installer; do not purge. If a provider registration is damaged, uninstall that provider without `--purge`, then reinstall it.

## Publish a release

The release workflow runs when a tag matching `v*` is pushed. It requires the tag to equal `v` plus the contents of `VERSION`, builds `boardroom.tar.gz` and `boardroom.zip`, and creates a GitHub Release with generated notes.

```bash
# After updating VERSION and merging a release-ready commit:
git tag v1.2.0
git push origin v1.2.0
```

The remote installers always download the assets from the latest published release. Test release candidates before moving the latest release pointer.

## Updating social playbooks

Social playbooks have a 30-day review interval. When an applicable playbook is older than that:

- Recheck official platform availability, products, policies, recommendation guidance, analytics, formats, and regional constraints.
- Update claims and source provenance.
- Change the reviewed date and increment the version for material changes.
- Run validation.

Expiry is a research trigger, not proof that every statement is wrong.

## Connected tools and MCP

Boardroom treats MCP as a source of live data or controlled actions, not as the location of council reasoning. Examples include analytics, design tools, cloud accounts, CRM data, documents, or browser research.

The UX specialist may inspect available tools and use relevant ones when authorized. Every specialist must still obey data minimization and approval gates. Connecting a tool does not authorize publishing, spending, deployment, account changes, or third-party communication.

## Validation and tests

Validate indexes, metadata, source IDs, dates, and local Markdown links:

```bash
python3 scripts/validate_boardroom.py
```

Run the repository tests:

```bash
python3 -m unittest discover -s tests -v
```

Validate the individual skill bundles with OpenAI's skill creator validator when it is installed:

```bash
python3 /path/to/skill-creator/scripts/quick_validate.py skills/boardroom
python3 /path/to/skill-creator/scripts/quick_validate.py skills/create-boardroom-employee
```

## Repository map

```text
.
├── AGENTS.md                         # Codex project entry instruction
├── CLAUDE.md                         # Claude Code project entry instruction
├── skills/
│   ├── boardroom/                    # Team Lead workflow
│   └── create-boardroom-employee/    # controlled learning workflow
├── core/
│   ├── council/                      # council index and employee profiles
│   ├── playbooks/                    # selectively loaded specialist knowledge
│   ├── protocols/                    # orchestration, research, governance, quality
│   ├── schemas/                      # engagement and knowledge contracts
│   ├── templates/                    # engagement and specialist artifacts
│   └── sources.md                    # provenance registry
├── adapters/
│   ├── codex/
│   └── claude-code/
├── scripts/
│   ├── install_global.py             # global installation and safe upgrades
│   ├── uninstall_global.py           # safe unregister and optional purge
│   ├── check_prereqs.py              # platform, Python, CLI and write checks
│   ├── boardroom_home.py             # global home resolution and diagnostics
│   ├── record_knowledge_change.py    # durable-learning audit log
│   ├── package_boardroom.py
│   └── validate_boardroom.py
├── tests/
└── examples/
```

## Safety and professional boundaries

Boardroom provides structured decision support and does not claim professional licensure. Legal, tax, investment, insurance, medical, employment, and regulated compliance decisions require current jurisdiction-specific information and qualified professional review.

The Team Lead must obtain explicit approval before external side effects such as spending, publishing, messaging, deployment, production changes, account creation, or accepting terms. Analysis permission is not execution permission.

## License

Boardroom is available under the [MIT License](LICENSE).

## Contributing

Contributions use feature branches, Conventional Commits, pull-request review, and required cross-platform CI. Read [CONTRIBUTING.md](CONTRIBUTING.md) before starting a change.

## Design principles

- Progressive discovery over giant prompts.
- Smallest sufficient council over persona theater.
- Evidence and explicit assumptions over confident invention.
- Integrated decisions over concatenated reports.
- Provider-neutral capabilities over frozen model names.
- Reversible tests before expensive commitments.
- Auditable learning over silent self-modification.
