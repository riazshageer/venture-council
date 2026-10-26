#!/usr/bin/env python3
"""Validate Boardroom indexes, metadata, sources, and local Markdown links."""

from __future__ import annotations

import datetime as dt
import argparse
import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
LINK = re.compile(r"\[[^]]*\]\(([^)]+)\)")
SOURCE_ROW = re.compile(r"^\| ([A-Z][A-Z0-9-]+) \|", re.MULTILINE)


def frontmatter(path: Path) -> dict[str, str]:
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---\n"):
        return {}
    block = text.split("---\n", 2)[1]
    result: dict[str, str] = {}
    for line in block.splitlines():
        if ":" in line:
            key, value = line.split(":", 1)
            result[key.strip()] = value.strip()
    return result


def source_ids(raw: str) -> set[str]:
    return {item.strip() for item in raw.strip("[]").split(",") if item.strip()}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--core", type=Path, help="Validate an installed global core instead of the source tree")
    args = parser.parse_args()
    core = args.core.resolve() if args.core else ROOT / "core"
    errors: list[str] = []
    sources_text = (core / "sources.md").read_text(encoding="utf-8")
    known_sources = set(SOURCE_ROW.findall(sources_text))
    knowledge = sorted((core / "council/employees").glob("*.md"))
    knowledge += sorted((core / "playbooks").glob("*/*.md"))
    seen_ids: dict[str, Path] = {}

    for path in knowledge:
        data = frontmatter(path)
        for key in ("id", "status", "version", "reviewed", "review_interval_days", "source_ids"):
            if not data.get(key):
                errors.append(f"{path.relative_to(core)}: missing {key}")
        artifact_id = data.get("id")
        if artifact_id:
            if artifact_id in seen_ids:
                errors.append(f"duplicate id {artifact_id}: {seen_ids[artifact_id]} and {path}")
            seen_ids[artifact_id] = path
        if data.get("status") not in {"candidate", "active", "deprecated"}:
            errors.append(f"{path.relative_to(core)}: invalid status {data.get('status')}")
        try:
            dt.date.fromisoformat(data.get("reviewed", ""))
            if int(data.get("review_interval_days", "0")) <= 0:
                raise ValueError
        except ValueError:
            errors.append(f"{path.relative_to(core)}: invalid review metadata")
        for source in source_ids(data.get("source_ids", "")) - known_sources:
            errors.append(f"{path.relative_to(core)}: unknown source {source}")

    scan_root = core if args.core else ROOT
    for path in scan_root.rglob("*.md"):
        if any(part in {".git", "dist"} for part in path.parts):
            continue
        for target in LINK.findall(path.read_text(encoding="utf-8")):
            if target.startswith(("http://", "https://", "#", "mailto:")):
                continue
            clean = target.split("#", 1)[0]
            if clean and not (path.parent / clean).resolve().exists():
                errors.append(f"{path.relative_to(scan_root)}: broken link {target}")

    if not args.core:
        required_skill = {"name", "description"}
        for path in (ROOT / "skills").glob("*/SKILL.md"):
            missing = required_skill - frontmatter(path).keys()
            if missing:
                errors.append(f"{path.relative_to(ROOT)}: missing {', '.join(sorted(missing))}")

    if errors:
        print("Boardroom validation failed:")
        for error in errors:
            print(f"- {error}")
        return 1
    print(f"Boardroom validation passed: {len(knowledge)} knowledge artifacts, {len(known_sources)} sources")
    return 0


if __name__ == "__main__":
    sys.exit(main())
