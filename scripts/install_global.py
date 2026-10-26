#!/usr/bin/env python3
"""Install Boardroom globally while preserving learned global knowledge."""

from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import json
import os
import shutil
import subprocess
import sys
from pathlib import Path

from boardroom_home import boardroom_home


ROOT = Path(__file__).resolve().parents[1]
RUNTIME_ITEMS = ("skills", "scripts", "adapters", "AGENTS.md", "CLAUDE.md", "VERSION")


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def files_under(root: Path) -> dict[Path, Path]:
    if not root.exists():
        return {}
    return {path.relative_to(root): path for path in root.rglob("*") if path.is_file()}


def install_runtime(home: Path) -> None:
    app = home / "app"
    staging = home / ".app-staging"
    if staging.exists():
        shutil.rmtree(staging)
    staging.mkdir(parents=True)
    for name in RUNTIME_ITEMS:
        source = ROOT / name
        target = staging / name
        if source.is_dir():
            shutil.copytree(source, target)
        else:
            shutil.copy2(source, target)
    if app.exists():
        shutil.rmtree(app)
    staging.rename(app)


def merge_core(home: Path) -> list[str]:
    new_root = ROOT / "core"
    live_root = home / "core"
    old_root = home / "bundled-core"
    conflicts_root = home / "conflicts" / dt.datetime.now().strftime("%Y%m%dT%H%M%S")
    changes: list[str] = []

    new_files = files_under(new_root)
    old_files = files_under(old_root)
    live_files = files_under(live_root)
    for relative, new_file in new_files.items():
        live_file = live_root / relative
        old_file = old_files.get(relative)
        if relative not in live_files:
            live_file.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(new_file, live_file)
            changes.append(f"added {relative}")
        elif old_file and digest(live_file) == digest(old_file):
            if digest(live_file) != digest(new_file):
                shutil.copy2(new_file, live_file)
                changes.append(f"updated {relative}")
        elif old_file and digest(new_file) != digest(old_file) and digest(live_file) != digest(new_file):
            conflict = conflicts_root / relative
            conflict.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(new_file, conflict)
            changes.append(f"preserved learned version; new bundled copy at conflicts/{conflicts_root.name}/{relative}")

    if old_root.exists():
        shutil.rmtree(old_root)
    shutil.copytree(new_root, old_root)
    return changes


def replace_link(link: Path, target: Path, force: bool) -> None:
    if link.is_symlink():
        if link.resolve() == target.resolve():
            return
        link.unlink()
    elif link.exists():
        if not force:
            raise SystemExit(f"Refusing to replace existing path: {link}. Re-run with --force.")
        backup = link.with_name(f"{link.name}.backup-{dt.datetime.now().strftime('%Y%m%dT%H%M%S')}")
        link.rename(backup)
    link.parent.mkdir(parents=True, exist_ok=True)
    link.symlink_to(target)


def install_provider(home: Path, provider: str, force: bool) -> list[str]:
    installed: list[str] = []
    if provider in {"codex", "all"}:
        codex_base = Path(os.environ.get("CODEX_HOME", Path.home() / ".codex")) / "skills"
        for name in ("boardroom", "create-boardroom-employee"):
            link = codex_base / name
            replace_link(link, home / "app" / "skills" / name, force)
            installed.append(str(link))
    if provider in {"claude", "all"}:
        claude_base = Path.home() / ".claude"
        for name in ("boardroom", "create-boardroom-employee"):
            link = claude_base / "skills" / name
            replace_link(link, home / "app" / "skills" / name, force)
            installed.append(str(link))
        for agent in (home / "app" / "adapters" / "claude-code" / "agents").glob("*.md"):
            link = claude_base / "agents" / agent.name
            replace_link(link, agent, force)
            installed.append(str(link))
    return installed


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--provider", choices=("codex", "claude", "all"), default="all")
    parser.add_argument("--force", action="store_true", help="Back up and replace conflicting provider paths")
    args = parser.parse_args()

    home = boardroom_home()
    home.mkdir(parents=True, exist_ok=True)
    (home / "audit").mkdir(exist_ok=True)
    changes = merge_core(home)
    install_runtime(home)
    installed = install_provider(home, args.provider, args.force)
    version = (ROOT / "VERSION").read_text(encoding="utf-8").strip()
    manifest = {
        "version": version,
        "installed_at": dt.datetime.now(dt.timezone.utc).isoformat(),
        "source": str(ROOT),
        "provider": args.provider,
        "home": str(home),
    }
    (home / "installation.json").write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    subprocess.run(
        [sys.executable, str(home / "app" / "scripts" / "validate_boardroom.py"), "--core", str(home / "core")],
        check=True,
    )
    print(json.dumps({"installation": manifest, "knowledge_changes": changes, "links": installed}, indent=2))


if __name__ == "__main__":
    main()
