#!/usr/bin/env python3
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PROBLEMS = ROOT / "problems"
ALLOWED = {"verified", "unverified", "missing"}


def fail(message: str) -> None:
    print(f"ERROR: {message}", file=sys.stderr)
    raise SystemExit(1)


def main() -> None:
    if not PROBLEMS.exists():
        print("No problem directories committed yet; infrastructure is valid.")
        return

    for meta in PROBLEMS.glob("*/metadata.json"):
        try:
            number = int(meta.parent.name)
        except ValueError:
            fail(f"Non-numeric problem directory: {meta.parent}")
        if not 3000 <= number <= 4000:
            fail(f"Problem outside requested range: {number}")
        data = json.loads(meta.read_text(encoding="utf-8"))
        if data.get("number") != number:
            fail(f"metadata number mismatch in {meta}")
        if data.get("status", "missing") not in ALLOWED:
            fail(f"invalid status in {meta}")
        for language, status in data.get("languages", {}).items():
            if status not in ALLOWED:
                fail(f"invalid language status {language}={status} in {meta}")

    print("Metadata validation passed.")


if __name__ == "__main__":
    main()
