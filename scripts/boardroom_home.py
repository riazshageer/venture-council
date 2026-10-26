#!/usr/bin/env python3
"""Resolve and inspect Boardroom's global application data directory."""

from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path


def boardroom_home() -> Path:
    explicit = os.environ.get("BOARDROOM_HOME")
    if explicit:
        return Path(explicit).expanduser().resolve()
    if sys.platform == "win32":
        local_app_data = os.environ.get("LOCALAPPDATA")
        base = Path(local_app_data) if local_app_data else Path.home() / "AppData" / "Local"
        return (base / "Boardroom").resolve()
    xdg_data = os.environ.get("XDG_DATA_HOME")
    base = Path(xdg_data).expanduser() if xdg_data else Path.home() / ".local" / "share"
    return (base / "boardroom").resolve()


def resolved_paths(require_initialized: bool = True) -> dict[str, str]:
    home = boardroom_home()
    paths = {
        "home": str(home),
        "core": str(home / "core"),
        "council_index": str(home / "core" / "council" / "index.md"),
        "employees": str(home / "core" / "council" / "employees"),
        "playbook_index": str(home / "core" / "playbooks" / "index.md"),
        "playbooks": str(home / "core" / "playbooks"),
        "protocols": str(home / "core" / "protocols"),
        "schemas": str(home / "core" / "schemas"),
        "templates": str(home / "core" / "templates"),
        "sources": str(home / "core" / "sources.md"),
        "audit_log": str(home / "audit" / "knowledge-changes.jsonl"),
        "runtime": str(home / "app"),
        "manifest": str(home / "installation.json"),
    }
    if require_initialized and not Path(paths["council_index"]).is_file():
        raise SystemExit(
            f"Boardroom is not initialized at {home}. "
            "Run: python3 scripts/install_global.py --provider all"
        )
    return paths


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("command", choices=("home", "paths", "check"), nargs="?", default="paths")
    parser.add_argument("--allow-uninitialized", action="store_true")
    args = parser.parse_args()
    if args.command == "home":
        print(boardroom_home())
        return
    paths = resolved_paths(require_initialized=not args.allow_uninitialized)
    if args.command == "check":
        manifest = Path(paths["manifest"])
        result = {"initialized": manifest.is_file(), **paths}
        if manifest.is_file():
            result["installation"] = json.loads(manifest.read_text(encoding="utf-8"))
        print(json.dumps(result, indent=2))
        return
    print(json.dumps(paths, indent=2))


if __name__ == "__main__":
    main()
