# Claude Code adapter

Install Boardroom into its global application home and register its user-scoped Claude Code skills and optional agents:

```bash
python3 scripts/install_global.py --provider claude
```

The default application home is `${XDG_DATA_HOME}/boardroom` when set, otherwise `~/.local/share/boardroom`. Set `BOARDROOM_HOME` to choose another location. The installer links skills into `~/.claude/skills` and Boardroom's optional agents into `~/.claude/agents`.

For a packaged install, run:

```bash
python3 scripts/package_boardroom.py claude dist/boardroom-claude
```

The generated directory is also a complete global installer source. After extracting it, run its `scripts/install_global.py --provider claude` command. Installing only the plugin manifest does not initialize the writable global knowledge store.

The optional generic specialist, researcher, and critic agents isolate bounded work. The Team Lead alone staffs meetings, controls transitions, reconciles, and answers the user. Map capability tiers only to models currently available in the installation.
