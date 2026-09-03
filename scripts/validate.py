#!/usr/bin/env python3
from __future__ import annotations

import json
import sys
from pathlib import Path

from locked_sources import get_sources

ROOT = Path(__file__).resolve().parents[1]
PROBLEMS = ROOT / "problems"
START, END = 3000, 4000
EXPECTED = set(range(START, END + 1))
ALLOWED = {
    "verified",
    "unverified",
    "missing",
    "partially-verified",
    "imported-unverified",
    "translated-unverified",
}
SOLUTION_SUFFIXES = {
    ".py", ".cpp", ".cc", ".cxx", ".c", ".java", ".go", ".rs", ".ts",
    ".js", ".cs", ".php", ".rb", ".swift", ".scala", ".dart", ".kt",
    ".rkt", ".erl", ".ex", ".sql",
}


def fail(message: str) -> None:
    print(f"ERROR: {message}", file=sys.stderr)
    raise SystemExit(1)


def solution_files(problem_dir: Path) -> list[Path]:
    return sorted(
        p for p in problem_dir.iterdir()
        if p.is_file() and p.suffix.lower() in SOLUTION_SUFFIXES and p.stat().st_size > 0
    )


def main() -> None:
    get_sources()
    canonical = json.loads((ROOT / "languages.json").read_text(encoding="utf-8"))
    if len(set(canonical.values())) != len(canonical):
        fail("languages.json has duplicate canonical filenames")
    if not PROBLEMS.exists():
        fail("problems/ directory is missing")

    seen: set[int] = set()
    metadata_count = 0
    solution_count = 0

    for meta in sorted(PROBLEMS.glob("*/metadata.json")):
        metadata_count += 1
        try:
            number = int(meta.parent.name)
        except ValueError:
            fail(f"Non-numeric problem directory: {meta.parent}")

        if number not in EXPECTED:
            fail(f"Problem outside requested range: {number}")
        if number in seen:
            fail(f"Duplicate problem metadata for {number}")
        seen.add(number)

        try:
            data = json.loads(meta.read_text(encoding="utf-8"))
        except Exception as exc:
            fail(f"Invalid JSON in {meta}: {exc}")

        if data.get("number") != number:
            fail(f"metadata number mismatch in {meta}")

        status = data.get("status", "missing")
        if status not in ALLOWED:
            fail(f"invalid status {status!r} in {meta}")

        for language, language_status in data.get("languages", {}).items():
            if language not in canonical:
                fail(f"Unknown/noncanonical language {language!r} in {meta}")
            if language_status not in ALLOWED:
                fail(f"invalid language status {language}={language_status} in {meta}")
            path = meta.parent / canonical[language]
            if not path.is_file() or not path.stat().st_size:
                fail(f"Declared language {language} has no non-empty canonical file in {meta.parent}")

        files = solution_files(meta.parent)
        if not files:
            fail(f"Problem {number} has no non-empty solution file")
        if not any(path.suffix == ".sql" for path in files):
            for required in ("cpp", "java"):
                if required not in data.get("languages", {}):
                    fail(f"Algorithm problem {number} is missing mandatory {required}")
        for language, language_status in data.get("languages", {}).items():
            if language_status == "translated-unverified" and language not in data.get("adapted_sources", {}):
                fail(f"Translated language {number}/{language} has no explicit adaptation record")
        solution_count += len(files)
        for path in files:
            matches = [language for language, filename in canonical.items() if filename == path.name]
            if not matches:
                fail(f"Noncanonical solution filename: {path}")
            if matches[0] not in data.get("languages", {}):
                fail(f"Solution file has no metadata language entry: {path}")

        # Every imported solution must retain source attribution.
        if any(v == "imported-unverified" for v in data.get("languages", {}).values()):
            if not data.get("upstream") and not data.get("secondary_upstream") and not data.get("additional_sources"):
                fail(f"Problem {number} contains imported code without attribution")

    missing = sorted(EXPECTED - seen)
    if missing:
        fail(f"Missing metadata directories for {len(missing)} IDs: {missing[:20]}")

    if metadata_count != len(EXPECTED):
        fail(f"Expected {len(EXPECTED)} metadata files, found {metadata_count}")

    print(
        f"Archive validation passed: {metadata_count}/{len(EXPECTED)} problems, "
        f"{solution_count} non-empty solution files."
    )


if __name__ == "__main__":
    main()
