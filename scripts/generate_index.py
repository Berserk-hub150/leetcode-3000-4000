#!/usr/bin/env python3
"""Generate a complete index from actual canonical files, including imported variants."""
from __future__ import annotations

import argparse
from pathlib import Path

from archive import ROOT, inventory, statistics


def render(root: Path = ROOT) -> str:
    _, problems = inventory(root)
    stats = statistics(problems)
    lines = [
        "# Solution Index", "",
        f"**Problems with implementations:** {stats['covered']} / 1001", "",
        f"**Canonical solution files:** {stats['files']}", "",
        f"**Algorithm problems:** {stats['algorithms']} · **Database problems:** {stats['database']}",
        "",
        "Every link below points to a real non-empty canonical file. Imported files are",
        "included. Source integrity, compilation, behavioral tests and LeetCode judge",
        "submissions are distinct checks; see [VERIFICATION.md](VERIFICATION.md).",
        "",
        "| # | Problem | Type | Implementations |",
        "|---:|---|---|---|",
    ]
    for problem in problems:
        data = problem["metadata"]
        number = data["number"]
        title = (data.get("title") or "Unknown title").replace("|", "\\|")
        label = f"[{title}]({data['url']})" if data.get("url") else title
        links = " · ".join(
            f"[{language}](problems/{number}/{filename})"
            for language, filename in problem["files"].items()
        )
        kind = "SQL/database" if problem["database"] else "Algorithm"
        lines.append(f"| {number} | {label} | {kind} | {links} |")
    return "\n".join(lines) + "\n"


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    target = ROOT / "INDEX.md"
    content = render()
    if args.check:
        if not target.exists() or target.read_text(encoding="utf-8") != content:
            raise SystemExit("INDEX.md is stale; run python scripts/generate_index.py")
        print("INDEX.md is current")
    else:
        target.write_text(content, encoding="utf-8")
        print("Regenerated INDEX.md from the complete file inventory")


if __name__ == "__main__":
    main()
