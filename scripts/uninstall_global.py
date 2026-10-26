#!/usr/bin/env python3
"""Unregister Boardroom globally and optionally remove its application data."""

from __future__ import annotations

import argparse
import json
import os
import shutil
from pathlib import Path

from boardroom_home import boardroom_home


MANAGED_MARKER = ".boardroom-managed.json"


def remove_directory(path: Path, expected_target: Path, removed: list[str], skipped: list[str]) -> None:
    if path.is_symlink():
        if path.resolve() == expected_target.resolve():
            path.unlink()
            removed.append(str(path))
        else:
            skipped.append(f"{path}: symlink target is not this Boardroom installation")
    elif path.is_dir() and (path / MANAGED_MARKER).is_file():
        shutil.rmtree(path)
        removed.append(str(path))
    elif path.exists():
        skipped.append(f"{path}: not marked as Boardroom-managed")


def remove_file(path: Path, expected_target: Path, removed: list[str], skipped: list[str]) -> None:
    marker = path.with_name(path.name + ".boardroom-managed")
    if path.is_symlink():
        if path.resolve() == expected_target.resolve():
            path.unlink()
            removed.append(str(path))
        else:
            skipped.append(f"{path}: symlink target is not this Boardroom installation")
    elif path.is_file() and marker.is_file():
        path.unlink()
        marker.unlink()
        removed.append(str(path))
    elif path.exists():
        skipped.append(f"{path}: not marked as Boardroom-managed")


def unregister(home: Path, provider: str) -> tuple[list[str], list[str]]:
    removed: list[str] = []
    skipped: list[str] = []
    if provider in {"codex", "all"}:
        codex_base = Path(os.environ.get("CODEX_HOME", Path.home() / ".codex")) / "skills"
        for name in ("boardroom", "create-boardroom-employee"):
            remove_directory(codex_base / name, home / "app" / "skills" / name, removed, skipped)
    if provider in {"claude", "all"}:
        claude_base = Path.home() / ".claude"
        for name in ("boardroom", "create-boardroom-employee"):
            remove_directory(claude_base / "skills" / name, home / "app" / "skills" / name, removed, skipped)
        agents = home / "app" / "adapters" / "claude-code" / "agents"
        for name in ("boardroom-critic.md", "boardroom-researcher.md"):
            remove_file(claude_base / "agents" / name, agents / name, removed, skipped)
    return removed, skipped


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--provider", choices=("codex", "claude", "all"), default="all")
    parser.add_argument("--purge", action="store_true", help="Also delete global knowledge, audit history, and backups")
    parser.add_argument("--yes", action="store_true", help="Confirm destructive --purge without an interactive prompt")
    args = parser.parse_args()

    home = boardroom_home()
    removed, skipped = unregister(home, args.provider)
    purged = False
    if args.purge and home.exists():
        if not args.yes:
            answer = input(f"Permanently delete all Boardroom data at {home}? [y/N] ").strip().lower()
            if answer not in {"y", "yes"}:
                raise SystemExit("Purge cancelled; provider registrations were removed but global data was preserved.")
        shutil.rmtree(home)
        purged = True

    print(json.dumps({
        "removed": removed,
        "skipped": skipped,
        "global_data": str(home),
        "purged": purged,
        "note": "Global knowledge was preserved." if not purged else "Global knowledge was permanently deleted.",
    }, indent=2))


if __name__ == "__main__":
    main()
