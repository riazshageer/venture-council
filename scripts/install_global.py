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
from check_prereqs import check as check_prerequisites


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


MANAGED_MARKER = ".boardroom-managed.json"


def managed_directory(path: Path) -> bool:
    return path.is_dir() and (path / MANAGED_MARKER).is_file()


def managed_file(path: Path) -> bool:
    return path.is_file() and path.with_name(path.name + ".boardroom-managed").is_file()


def back_up(path: Path) -> Path:
    backup = path.with_name(f"{path.name}.backup-{dt.datetime.now().strftime('%Y%m%dT%H%M%S')}")
    path.rename(backup)
    return backup


def install_directory(destination: Path, target: Path, force: bool) -> None:
    if os.name != "nt":
        if destination.is_symlink():
            if destination.resolve() == target.resolve():
                return
            destination.unlink()
        elif destination.exists():
            if not force:
                raise SystemExit(f"Refusing to replace existing path: {destination}. Re-run with --force.")
            back_up(destination)
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.symlink_to(target, target_is_directory=True)
        return

    if destination.exists():
        if not managed_directory(destination):
            if not force:
                raise SystemExit(f"Refusing to replace existing path: {destination}. Re-run with --force.")
            back_up(destination)
        else:
            shutil.rmtree(destination)
    shutil.copytree(target, destination)
    (destination / MANAGED_MARKER).write_text(
        json.dumps({"managed_by": "boardroom", "source": str(target)}) + "\n",
        encoding="utf-8",
    )


def install_file(destination: Path, target: Path, force: bool) -> None:
    marker = destination.with_name(destination.name + ".boardroom-managed")
    if destination.exists() or destination.is_symlink():
        owned = destination.is_symlink() or managed_file(destination)
        if not owned and not force:
            raise SystemExit(f"Refusing to replace existing path: {destination}. Re-run with --force.")
        if destination.is_dir() and not destination.is_symlink():
            back_up(destination)
        else:
            if not owned:
                back_up(destination)
            else:
                destination.unlink()
        marker.unlink(missing_ok=True)
    destination.parent.mkdir(parents=True, exist_ok=True)
    if os.name == "nt":
        shutil.copy2(target, destination)
        marker.write_text("managed by Boardroom\n", encoding="utf-8")
    else:
        destination.symlink_to(target)


def install_provider(home: Path, provider: str, force: bool) -> list[str]:
    installed: list[str] = []
    if provider in {"codex", "all"}:
        codex_base = Path(os.environ.get("CODEX_HOME", Path.home() / ".codex")) / "skills"
        for name in ("boardroom", "create-boardroom-employee"):
            link = codex_base / name
            install_directory(link, home / "app" / "skills" / name, force)
            installed.append(str(link))
    if provider in {"claude", "all"}:
        claude_base = Path.home() / ".claude"
        for name in ("boardroom", "create-boardroom-employee"):
            link = claude_base / "skills" / name
            install_directory(link, home / "app" / "skills" / name, force)
            installed.append(str(link))
        for agent in (home / "app" / "adapters" / "claude-code" / "agents").glob("*.md"):
            link = claude_base / "agents" / agent.name
            install_file(link, agent, force)
            installed.append(str(link))
    return installed


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--provider", choices=("codex", "claude", "all"), default="all")
    parser.add_argument("--force", action="store_true", help="Back up and replace conflicting provider paths")
    parser.add_argument("--skip-prereq-check", action="store_true")
    args = parser.parse_args()

    if not args.skip_prereq_check:
        result, ok = check_prerequisites(args.provider)
        if not ok:
            print(json.dumps(result, indent=2))
            raise SystemExit("Prerequisite check failed. Fix the reported items or use --skip-prereq-check.")

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
