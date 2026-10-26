#!/usr/bin/env python3
"""Print paths to Boardroom's initialized global knowledge store."""

from __future__ import annotations

import json
import os
import sys
from pathlib import Path


explicit = os.environ.get("BOARDROOM_HOME")
xdg_data = os.environ.get("XDG_DATA_HOME")
if explicit:
    home = Path(explicit).expanduser()
elif sys.platform == "win32":
    home = Path(os.environ.get("LOCALAPPDATA", Path.home() / "AppData" / "Local")) / "Boardroom"
else:
    home = (Path(xdg_data).expanduser() if xdg_data else Path.home() / ".local" / "share") / "boardroom"
core = home.resolve() / "core"
if not (core / "council" / "index.md").is_file():
    raise SystemExit(f"Boardroom global knowledge is not initialized at {home}. Run the global installer from the Boardroom distribution.")
print(json.dumps({
    "home": str(home.resolve()),
    "core": str(core),
    "council_index": str(core / "council" / "index.md"),
    "employees": str(core / "council" / "employees"),
    "playbook_index": str(core / "playbooks" / "index.md"),
    "playbooks": str(core / "playbooks"),
    "sources": str(core / "sources.md"),
    "audit_log": str(home.resolve() / "audit" / "knowledge-changes.jsonl"),
    "runtime": str(home.resolve() / "app"),
}, indent=2))
