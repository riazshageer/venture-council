#!/usr/bin/env python3
"""Assemble a provider-specific Boardroom plugin without duplicating its source."""

from __future__ import annotations

import argparse
import json
import shutil
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def copy_tree(source: Path, target: Path) -> None:
    if target.exists():
        shutil.rmtree(target)
    shutil.copytree(source, target)


def package(provider: str, destination: Path) -> None:
    if destination.exists() and any(destination.iterdir()):
        raise SystemExit(f"Destination must be absent or empty: {destination}")
    destination.mkdir(parents=True, exist_ok=True)

    copy_tree(ROOT / "core", destination / "core")
    copy_tree(ROOT / "skills", destination / "skills")
    copy_tree(ROOT / "scripts", destination / "scripts")
    copy_tree(ROOT / "adapters", destination / "adapters")
    shutil.copy2(ROOT / "VERSION", destination / "VERSION")
    shutil.copy2(ROOT / "AGENTS.md", destination / "AGENTS.md")
    shutil.copy2(ROOT / "CLAUDE.md", destination / "CLAUDE.md")

    adapter = ROOT / "adapters" / ("codex" if provider == "codex" else "claude-code")
    if provider == "codex":
        manifest_dir = destination / ".codex-plugin"
        manifest_name = "plugin.json"
    else:
        manifest_dir = destination / ".claude-plugin"
        manifest_name = "plugin.json"
        copy_tree(adapter / "agents", destination / "agents")

    manifest_dir.mkdir(parents=True, exist_ok=True)
    manifest = json.loads((adapter / "plugin.json").read_text(encoding="utf-8"))
    (manifest_dir / manifest_name).write_text(
        json.dumps(manifest, indent=2) + "\n", encoding="utf-8"
    )
    shutil.copy2(adapter / "capability-tiers.md", destination / "capability-tiers.md")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("provider", choices=("codex", "claude"))
    parser.add_argument("destination", type=Path)
    args = parser.parse_args()
    package(args.provider, args.destination.resolve())


if __name__ == "__main__":
    main()
