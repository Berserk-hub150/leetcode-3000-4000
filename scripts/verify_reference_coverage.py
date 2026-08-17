#!/usr/bin/env python3
from __future__ import annotations

import json
import subprocess
import tempfile
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PROBLEMS = ROOT / "problems"
START, END = 3000, 4000
UPSTREAM = "https://github.com/kamyu104/LeetCode-Solutions"

# Directory, extension, display language.
SOURCES = [
    ("Python3", ".py", "Python3"),
    ("Python", ".py", "Python"),
    ("C++", ".cpp", "C++"),
    ("Java", ".java", "Java"),
    ("Golang", ".go", "Go"),
    ("C#", ".cs", "C#"),
    ("Kotlin", ".kt", "Kotlin"),
    ("MySQL", ".sql", "MySQL"),
    ("PHP", ".php", "PHP"),
    ("Pandas", ".py", "Pandas"),
]


def run(*args: str, cwd: Path | None = None) -> None:
    subprocess.run(args, cwd=cwd, check=True, stdout=subprocess.DEVNULL)


def build_indexes(upstream: Path):
    indexes = []
    for dirname, extension, language in SOURCES:
        root = upstream / dirname
        paths = {}
        if root.exists():
            for path in root.rglob(f"*{extension}"):
                paths.setdefault(path.stem, path)
        indexes.append((language, paths))
    return indexes


def main() -> None:
    missing_metadata = []
    missing_reference = []
    by_language = Counter()
    covered = 0

    with tempfile.TemporaryDirectory(prefix="leetcode-reference-") as tmp:
        upstream = Path(tmp) / "LeetCode-Solutions"
        run("git", "clone", "--depth=1", "--filter=blob:none", UPSTREAM + ".git", str(upstream))
        indexes = build_indexes(upstream)

        for number in range(START, END + 1):
            meta_path = PROBLEMS / str(number) / "metadata.json"
            if not meta_path.exists():
                missing_metadata.append(number)
                continue
            data = json.loads(meta_path.read_text(encoding="utf-8"))
            slug = data.get("slug") or data.get("url", "").rstrip("/").split("/")[-1]
            if not slug:
                missing_reference.append(number)
                continue

            found_languages = []
            for language, index in indexes:
                if slug in index:
                    found_languages.append(language)
                    by_language[language] += 1

            if not found_languages:
                missing_reference.append(number)
            else:
                covered += 1

    lines = [
        "# Reference solution coverage",
        "",
        f"- Range: **{START}–{END}**",
        f"- Problems with at least one matching upstream solution: **{covered} / {END - START + 1}**",
        f"- Missing local metadata: **{len(missing_metadata)}**",
        f"- Missing upstream reference solution: **{len(missing_reference)}**",
        "",
        "## Matching reference files by language",
        "",
    ]
    for language, count in by_language.most_common():
        lines.append(f"- {language}: {count}")
    lines.extend(["", "## Missing reference IDs", ""])
    lines.append(", ".join(map(str, missing_reference)) if missing_reference else "None")
    (ROOT / "REFERENCE_COVERAGE.md").write_text("\n".join(lines) + "\n", encoding="utf-8")

    if missing_metadata or missing_reference:
        raise SystemExit(
            f"Reference coverage failed: metadata_missing={len(missing_metadata)}, "
            f"reference_missing={len(missing_reference)}"
        )

    print(f"Reference coverage passed: {covered}/{END - START + 1} problem slugs matched upstream solutions.")


if __name__ == "__main__":
    main()
