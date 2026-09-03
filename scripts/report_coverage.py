#!/usr/bin/env python3
"""Generate live coverage counts from the same inventory as INDEX.md."""
from __future__ import annotations

import argparse
from pathlib import Path

from archive import ROOT, inventory, statistics


def render(root: Path = ROOT) -> str:
    _, problems = inventory(root)
    stats = statistics(problems)
    missing = sorted(set(range(3000, 4001)) - {
        p["metadata"]["number"] for p in problems if p["files"]
    })
    lines = [
        "# Coverage report", "",
        "- Range: **3000–4000**",
        f"- Problems with at least one solution: **{stats['covered']} / 1001**",
        f"- Canonical solution files: **{stats['files']}**",
        f"- Algorithm problems: **{stats['algorithms']}**",
        f"- SQL/database problems: **{stats['database']}**", "",
        "## Files by canonical language", "",
        "| Language | Files |", "|---|---:|",
    ]
    for language, count in stats["languages"].most_common():
        lines.append(f"| {language} | {count} |")
    lines.extend(["", "## Per-file metadata statuses", ""])
    for status, count in sorted(stats["statuses"].items()):
        lines.append(f"- `{status}`: {count}")
    lines.extend(["", "These are metadata statuses, not a count of authenticated Accepted submissions.",
                  "", "## C++ and Java applicability", "",
                  "LeetCode database tasks do not accept native C++/Java submissions.",
                  "They are listed separately, not filled with placeholders.", ""])
    for language in ("cpp", "java"):
        pending = [p["metadata"]["number"] for p in problems
                   if not p["database"] and language not in p["files"]]
        complete = stats["algorithms"] - len(pending)
        lines.append(f"- {language}: **{complete}/{stats['algorithms']}** applicable algorithm problems")
        if pending:
            lines.append("  - Missing: " + ", ".join(map(str, pending)))
    database_ids = [p["metadata"]["number"] for p in problems if p["database"]]
    lines.extend(["", "Database IDs: " + ", ".join(map(str, database_ids)), "",
                  "## Missing solution IDs", "", ", ".join(map(str, missing)) if missing else "None."])
    return "\n".join(lines) + "\n"


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    target = ROOT / "COVERAGE.md"
    content = render()
    if args.check:
        if not target.exists() or target.read_text(encoding="utf-8") != content:
            raise SystemExit("COVERAGE.md is stale; run python scripts/report_coverage.py")
        print("COVERAGE.md is current")
    else:
        target.write_text(content, encoding="utf-8")
        print("Regenerated COVERAGE.md")


if __name__ == "__main__":
    main()
