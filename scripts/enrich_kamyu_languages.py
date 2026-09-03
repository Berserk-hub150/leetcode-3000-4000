#!/usr/bin/env python3
"""Add missing language variants from kamyu104/LeetCode-Solutions.

This is an enrichment pass: it scans all LeetCode problems 3000..4000 and copies
an upstream implementation only when the corresponding local language file does
not already exist. Existing local or doocs-derived files are never overwritten.
"""
from __future__ import annotations

import json
import subprocess
import tempfile
from collections import Counter
from pathlib import Path

from locked_sources import clone_locked

ROOT = Path(__file__).resolve().parents[1]
PROBLEMS = ROOT / "problems"
START, END = 3000, 4000
UPSTREAM_REPO = "kamyu104/LeetCode-Solutions"
UPSTREAM_URL = "https://github.com/kamyu104/LeetCode-Solutions"

# Ordered so a modern Python3 solution wins over the legacy Python directory.
SOURCES = [
    ("Python3", ".py", "python", "python.py"),
    ("Python", ".py", "python", "python.py"),
    ("C++", ".cpp", "cpp", "cpp.cpp"),
    ("Java", ".java", "java", "java.java"),
    ("Golang", ".go", "go", "go.go"),
    ("C#", ".cs", "csharp", "csharp.cs"),
    ("Kotlin", ".kt", "kotlin", "kotlin.kt"),
    ("MySQL", ".sql", "mysql", "mysql.sql"),
    ("PHP", ".php", "php", "php.php"),
]


def run(*args: str, cwd: Path | None = None) -> None:
    subprocess.run(args, cwd=cwd, check=True)


def build_indexes(upstream: Path):
    indexes = []
    for dirname, extension, language, local_name in SOURCES:
        source_dir = upstream / dirname
        index = {}
        if source_dir.exists():
            for path in source_dir.rglob(f"*{extension}"):
                index.setdefault(path.stem, path)
        indexes.append((language, local_name, index))
    return indexes


def main() -> None:
    added_files = 0
    enriched_problems = set()
    by_language = Counter()

    with tempfile.TemporaryDirectory(prefix="leetcode-kamyu-enrich-") as tmp:
        upstream = Path(tmp) / "LeetCode-Solutions"
        clone_locked("kamyu", upstream)
        indexes = build_indexes(upstream)

        for number in range(START, END + 1):
            target = PROBLEMS / str(number)
            metadata_path = target / "metadata.json"
            if not metadata_path.exists():
                continue
            try:
                metadata = json.loads(metadata_path.read_text(encoding="utf-8"))
            except Exception:
                continue

            slug = metadata.get("slug")
            if not slug:
                url = metadata.get("url", "").rstrip("/")
                slug = url.split("/")[-1] if url else None
            if not slug:
                continue

            metadata.setdefault("languages", {})
            source_record = metadata.setdefault("secondary_upstream", {
                "repository": UPSTREAM_REPO,
                "url": UPSTREAM_URL,
                "license": "MIT",
                "copyright": "Copyright (c) 2018 https://github.com/kamyu104/LeetCode-Solutions",
                "files": {},
            })
            if source_record.get("repository") == UPSTREAM_REPO:
                source_record.setdefault("files", {})

            seen_local_names = set()
            changed = False
            for language, local_name, index in indexes:
                # Python3 and Python map to the same local file. Check it once.
                if local_name in seen_local_names:
                    continue
                source = index.get(slug)
                if source is None:
                    continue
                output = target / local_name
                if output.exists():
                    seen_local_names.add(local_name)
                    continue

                output.write_bytes(source.read_bytes())
                metadata["languages"][language] = "imported-unverified"
                if source_record.get("repository") == UPSTREAM_REPO:
                    source_record["files"][language] = str(source.relative_to(upstream)).replace("\\", "/")
                added_files += 1
                by_language[language] += 1
                enriched_problems.add(number)
                changed = True
                seen_local_names.add(local_name)

            if changed:
                if metadata.get("status") == "verified":
                    metadata["status"] = "partially-verified"
                elif metadata.get("status") not in {"partially-verified"}:
                    metadata["status"] = "unverified"
                metadata_path.write_text(
                    json.dumps(metadata, indent=2, ensure_ascii=False) + "\n",
                    encoding="utf-8",
                )

    lines = [
        "# Language enrichment status",
        "",
        f"- Source: **{UPSTREAM_REPO}** (MIT)",
        f"- Problems receiving at least one additional language: **{len(enriched_problems)}**",
        f"- New language solution files added: **{added_files}**",
        "",
        "## Added files by language",
        "",
    ]
    if by_language:
        for language, count in by_language.most_common():
            lines.append(f"- {language}: {count}")
    else:
        lines.append("- No additional variants were available without overwriting existing files.")
    lines.extend([
        "",
        "Existing solution files were never overwritten. Added files remain `imported-unverified` until independently checked against the LeetCode judge.",
    ])
    (ROOT / "ENRICHMENT_STATUS.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
