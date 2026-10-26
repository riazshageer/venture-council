# Codex adapter

Install Boardroom into its global application home and register its user-scoped Codex skills:

```bash
python3 scripts/install_global.py --provider codex
```

The default application home is `${XDG_DATA_HOME}/boardroom` when set, otherwise `~/.local/share/boardroom`. Set `BOARDROOM_HOME` to choose another location. The installer links the skills into `${CODEX_HOME}/skills` or `~/.codex/skills`.

For a packaged install, run:

```bash
python3 scripts/package_boardroom.py codex dist/boardroom-codex
```

The generated directory is also a complete global installer source. After extracting it, run its `scripts/install_global.py --provider codex` command. Installing only the plugin manifest does not initialize the writable global knowledge store.

Boardroom uses the active Codex runtime's available subagent and research tools. Capability tiers are intentions, not hardcoded model IDs. If programmatic model routing and durable hosted sessions are required, wrap the same core in OpenAI's Agents API rather than duplicating council prompts.
