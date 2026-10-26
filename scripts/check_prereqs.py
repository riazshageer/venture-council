#!/usr/bin/env python3
"""Check whether this machine can install and run Boardroom."""

from __future__ import annotations

import argparse
import json
import os
import platform
import shutil
import sys
import tempfile
from pathlib import Path

from boardroom_home import boardroom_home


MINIMUM_PYTHON = (3, 10)


def writable_directory(path: Path) -> tuple[bool, str]:
    candidate = path
    while not candidate.exists() and candidate != candidate.parent:
        candidate = candidate.parent
    try:
        candidate.mkdir(parents=True, exist_ok=True)
        with tempfile.NamedTemporaryFile(dir=candidate, prefix=".boardroom-write-", delete=True):
            pass
        return True, str(candidate)
    except OSError as error:
        return False, f"{candidate}: {error}"


def check(provider: str) -> tuple[dict[str, object], bool]:
    python_ok = sys.version_info >= MINIMUM_PYTHON
    home = boardroom_home()
    home_ok, home_detail = writable_directory(home)
    commands = {
        "codex": shutil.which("codex"),
        "claude": shutil.which("claude"),
    }
    requested = ("codex", "claude") if provider == "all" else (provider,)
    missing = [name for name in requested if not commands[name]]
    provider_ok = any(commands[name] for name in requested) if provider == "all" else not missing
    result: dict[str, object] = {
        "ok": python_ok and home_ok and provider_ok,
        "platform": platform.platform(),
        "python": {
            "ok": python_ok,
            "version": platform.python_version(),
            "minimum": ".".join(map(str, MINIMUM_PYTHON)),
            "executable": sys.executable,
        },
        "boardroom_home": {"ok": home_ok, "path": str(home), "detail": home_detail},
        "commands": commands,
        "requested_provider": provider,
        "missing_commands": missing,
    }
    return result, bool(result["ok"])


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--provider", choices=("codex", "claude", "all"), default="all")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    result, ok = check(args.provider)
    if args.json:
        print(json.dumps(result, indent=2))
    else:
        print(f"Boardroom prerequisite check: {'PASS' if ok else 'FAIL'}")
        print(f"- Platform: {result['platform']}")
        python = result["python"]
        print(f"- Python: {python['version']} ({'ok' if python['ok'] else 'requires 3.10+'})")
        home = result["boardroom_home"]
        print(f"- Application home: {home['path']} ({'writable' if home['ok'] else 'not writable'})")
        for name, command in result["commands"].items():
            if name in (("codex", "claude") if args.provider == "all" else (args.provider,)):
                print(f"- {name}: {command or 'not found on PATH'}")
        if result["missing_commands"]:
            if args.provider == "all" and ok:
                print("Missing agents will still be registered and become available after their CLI is installed.")
            else:
                print("Install the missing agent CLI or select only the provider already installed.")
    raise SystemExit(0 if ok else 1)


if __name__ == "__main__":
    main()
