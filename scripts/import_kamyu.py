#!/usr/bin/env python3
"""Fill solution-less LeetCode 3000..4000 entries from kamyu104/LeetCode-Solutions.

The importer only touches problem directories that currently have no solution file.
Existing local/doocs implementations are never overwritten. Imported code is
MIT-licensed upstream code and is recorded as imported-unverified in metadata.
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

# Source directory, source extension, local language key, local filename.
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

SOLUTION_SUFFIXES = {
    ".py", ".cpp", ".java", ".go", ".ts", ".js", ".rs", ".cs", ".c",
    ".kt", ".swift", ".scala", ".dart", ".rb", ".php", ".rkt", ".erl",
    ".ex", ".sql",
}


def run(*args: str, cwd: Path | None = None) -> None:
    subprocess.run(args, cwd=cwd, check=True)


def has_solution(directory: Path) -> bool:
    if not directory.exists():
        return False
    return any(
        p.is_file() and p.suffix.lower() in SOLUTION_SUFFIXES
        for p in directory.iterdir()
    )


def build_source_indexes(upstream: Path):
    indexes = []
    for dirname, extension, language, local_name in SOURCES:
        source_dir = upstream / dirname
        index = {}
        if source_dir.exists():
            for path in source_dir.rglob(f"*{extension}"):
                index[path.stem] = path
        indexes.append((language, local_name, index))
    return indexes


def main() -> None:
    filled_problems = 0
    imported_files = 0
    by_language = Counter()
    still_missing = []

    with tempfile.TemporaryDirectory(prefix="leetcode-kamyu-") as tmp:
        upstream = Path(tmp) / "LeetCode-Solutions"
        clone_locked("kamyu", upstream)
        indexes = build_source_indexes(upstream)

        for number in range(START, END + 1):
            target = PROBLEMS / str(number)
            if has_solution(target):
                continue

            metadata_path = target / "metadata.json"
            if not metadata_path.exists():
                still_missing.append(number)
                continue
            try:
                metadata = json.loads(metadata_path.read_text(encoding="utf-8"))
            except Exception:
                still_missing.append(number)
                continue

            slug = metadata.get("slug")
            if not slug:
                still_missing.append(number)
                continue

            target.mkdir(parents=True, exist_ok=True)
            imported_paths = {}
            seen_languages = set()

            for language, local_name, index in indexes:
                # Python3 is listed before Python; don't replace it with Python2/legacy.
                if language in seen_languages:
                    continue
                source = index.get(slug)
                if source is None:
                    continue
                output = target / local_name
                if output.exists():
                    seen_languages.add(language)
                    continue
                output.write_bytes(source.read_bytes())
                imported_paths[language] = str(source.relative_to(upstream)).replace("\\", "/")
                seen_languages.add(language)
                imported_files += 1
                by_language[language] += 1

            if imported_paths:
                filled_problems += 1
                metadata.setdefault("languages", {})
                for language in imported_paths:
                    metadata["languages"][language] = "imported-unverified"
                metadata["status"] = "unverified"
                metadata["secondary_upstream"] = {
                    "repository": UPSTREAM_REPO,
                    "url": UPSTREAM_URL,
                    "license": "MIT",
                    "copyright": "Copyright (c) 2018 https://github.com/kamyu104/LeetCode-Solutions",
                    "files": imported_paths,
                }
                metadata_path.write_text(
                    json.dumps(metadata, indent=2, ensure_ascii=False) + "\n",
                    encoding="utf-8",
                )
            else:
                still_missing.append(number)

    lines = [
        "# Secondary import status",
        "",
        f"- Source: **{UPSTREAM_REPO}** (MIT)",
        f"- Previously solution-less problems filled: **{filled_problems}**",
        f"- New solution files imported: **{imported_files}**",
        f"- Problems still without a solution after this pass: **{len(still_missing)}**",
        "",
        "## Imported files by language",
        "",
    ]
    for language, count in by_language.most_common():
        lines.append(f"- {language}: {count}")
    lines.extend(["", "## Still missing IDs", ""])
    lines.append(", ".join(map(str, still_missing)) if still_missing else "None")
    lines.extend([
        "",
        "All imported files remain `imported-unverified` until independently checked against the LeetCode judge.",
    ])
    (ROOT / "SECONDARY_IMPORT_STATUS.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
