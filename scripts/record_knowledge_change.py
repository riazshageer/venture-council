#!/usr/bin/env python3
"""Append a validated global Boardroom knowledge change to its audit log."""

from __future__ import annotations

import argparse
import datetime as dt
import json
from pathlib import Path

from boardroom_home import resolved_paths


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("kind", choices=("employee", "playbook", "protocol"))
    parser.add_argument("artifact_id")
    parser.add_argument("version")
    parser.add_argument("summary")
    parser.add_argument("--engagement")
    args = parser.parse_args()
    paths = resolved_paths()
    record = {
        "timestamp": dt.datetime.now(dt.timezone.utc).isoformat(),
        "kind": args.kind,
        "artifact_id": args.artifact_id,
        "version": args.version,
        "summary": args.summary,
        "engagement": args.engagement,
    }
    audit = Path(paths["audit_log"])
    audit.parent.mkdir(parents=True, exist_ok=True)
    with audit.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(record, sort_keys=True) + "\n")
    print(json.dumps(record, indent=2))


if __name__ == "__main__":
    main()
