#!/usr/bin/env python3
"""Fail when Boardroom's progressively loaded instruction surfaces exceed budgets."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
WORD = re.compile(r"\S+")


def words(path: Path) -> int:
    return len(WORD.findall(path.read_text(encoding="utf-8")))


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    limits = {
        "skills/boardroom/SKILL.md": 475,
        "core/council/index.md": 240,
        "core/playbooks/index.md": 300,
        "core/protocols/memory-scopes.md": 180,
        "core/protocols/orchestration.md": 240,
        "core/protocols/quality-gates.md": 210,
        "core/protocols/research.md": 160,
        "core/templates/specialist-brief.md": 60,
        "core/templates/specialist-report.md": 35,
        "core/playbooks/business/foundational-reframing.md": 575,
    }
    counts = {name: words(ROOT / name) for name in limits}
    bootstrap = counts["skills/boardroom/SKILL.md"] + counts["core/council/index.md"]
    errors = [f"{name}: {counts[name]} words exceeds {limit}" for name, limit in limits.items() if counts[name] > limit]
    if bootstrap > 725:
        errors.append(f"consult bootstrap: {bootstrap} words exceeds 725")

    group_limits = {
        "skill": (ROOT / "skills", "*/SKILL.md", 475),
        "employee": (ROOT / "core/council/employees", "*.md", 250),
        "playbook": (ROOT / "core/playbooks", "*/*.md", 600),
        "protocol": (ROOT / "core/protocols", "*.md", 250),
        "template": (ROOT / "core/templates", "**/*.md", 250),
    }
    group_counts: dict[str, dict[str, int]] = {}
    for group, (directory, pattern, maximum) in group_limits.items():
        group_counts[group] = {}
        for path in sorted(directory.glob(pattern)):
            count = words(path)
            relative = str(path.relative_to(ROOT))
            group_counts[group][relative] = count
            if count > maximum:
                errors.append(f"{relative}: {count} words exceeds {group} maximum {maximum}")

    for name in ("AGENTS.md", "CLAUDE.md"):
        count = words(ROOT / name)
        if count > 120:
            errors.append(f"{name}: {count} words exceeds 120")

    result = {
        "direct_words": counts["skills/boardroom/SKILL.md"],
        "consult_bootstrap_words": bootstrap,
        "limits": {name: {"words": counts[name], "maximum": limit} for name, limit in limits.items()},
        "groups": group_counts,
        "status": "fail" if errors else "pass",
        "errors": errors,
    }
    if args.json:
        print(json.dumps(result, indent=2))
    else:
        print(f"Direct bootstrap: {result['direct_words']} words")
        print(f"Consult bootstrap: {bootstrap} words")
        for error in errors:
            print(f"- {error}")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
