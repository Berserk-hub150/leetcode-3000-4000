#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PROBLEMS = ROOT / "problems"
OUT = ROOT / "INDEX.md"


def main() -> None:
    rows = []
    verified_problems = 0
    verified_solutions = 0
    implementations = 0

    if PROBLEMS.exists():
        for meta_path in sorted(PROBLEMS.glob("*/metadata.json"), key=lambda p: int(p.parent.name)):
            data = json.loads(meta_path.read_text(encoding="utf-8"))
            langs = data.get("languages", {})
            verified = sorted(k for k, v in langs.items() if v == "verified")
            unverified = sorted(k for k, v in langs.items() if v == "unverified")
            verified_solutions += len(verified)
            implementations += len(verified) + len(unverified)
            if verified:
                verified_problems += 1
            number = data["number"]
            title = data.get("title") or "Pending metadata"
            url = data.get("url")
            label = f"[{title}]({url})" if url else title
            rows.append(f"| {number} | {label} | {', '.join(verified) or '—'} | {', '.join(unverified) or '—'} |")

    header = [
        "# Solution Index",
        "",
        f"**Verified problems:** {verified_problems} / 1001  ",
        f"**Verified language solutions:** {verified_solutions}  ",
        f"**Total implementations present:** {implementations}",
        "",
        "| # | Problem | Verified | Needs verification |",
        "|---:|---|---|---|",
    ]
    OUT.write_text("\n".join(header + rows) + "\n", encoding="utf-8")
    print(f"Wrote {OUT}")


if __name__ == "__main__":
    main()
