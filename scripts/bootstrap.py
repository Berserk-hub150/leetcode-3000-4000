#!/usr/bin/env python3
"""Create the local 3000..4000 problem skeleton without pretending it is solved."""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PROBLEMS = ROOT / "problems"
START, END = 3000, 4000


def main() -> None:
    PROBLEMS.mkdir(exist_ok=True)
    created = 0
    for number in range(START, END + 1):
        directory = PROBLEMS / str(number)
        directory.mkdir(exist_ok=True)
        metadata = directory / "metadata.json"
        if metadata.exists():
            continue
        metadata.write_text(
            json.dumps(
                {
                    "number": number,
                    "title": None,
                    "slug": None,
                    "url": None,
                    "difficulty": None,
                    "status": "missing",
                    "languages": {},
                },
                indent=2,
            ) + "\n",
            encoding="utf-8",
        )
        created += 1
    print(f"Created {created} metadata files; range contains {END - START + 1} problems.")


if __name__ == "__main__":
    main()
