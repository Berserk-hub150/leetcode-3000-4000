#!/usr/bin/env python3
from __future__ import annotations

import json
import re
import subprocess
import tempfile
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PROBLEMS = ROOT / "problems"
START, END = 3000, 4000
KAMYU = "https://github.com/kamyu104/LeetCode-Solutions"
DOOCS = "https://github.com/doocs/leetcode"

# Directory, extension, display language.
KAMYU_SOURCES = [
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

DOOCS_CODE_BLOCK_RE = re.compile(r"^####\s+[^\n]+\s*\n+```[^\n]*\n(.+?)\n```", re.MULTILINE | re.DOTALL)


def run(*args: str, cwd: Path | None = None) -> None:
    subprocess.run(args, cwd=cwd, check=True, stdout=subprocess.DEVNULL)


def build_kamyu_indexes(upstream: Path):
    indexes = []
    for dirname, extension, language in KAMYU_SOURCES:
        root = upstream / dirname
        paths = {}
        if root.exists():
            for path in root.rglob(f"*{extension}"):
                paths.setdefault(path.stem, path)
        indexes.append((language, paths))
    return indexes


def clone_doocs_sparse(destination: Path) -> None:
    run("git", "clone", "--depth=1", "--filter=blob:none", "--sparse", DOOCS + ".git", str(destination))
    buckets = [f"solution/{start:04d}-{start + 99:04d}" for start in range(3000, 4100, 100)]
    run("git", "sparse-checkout", "set", *buckets, cwd=destination)


def doocs_has_solution(upstream: Path, metadata: dict) -> bool:
    record = metadata.get("upstream") or {}
    if record.get("repository") != "doocs/leetcode":
        return False
    relative = record.get("path")
    if not relative:
        return False
    readme = upstream / relative / "README_EN.md"
    if not readme.exists():
        return False
    text = readme.read_text(encoding="utf-8", errors="replace")
    return any(block.strip() for block in DOOCS_CODE_BLOCK_RE.findall(text))


def main() -> None:
    missing_metadata = []
    missing_reference = []
    by_language = Counter()
    source_counts = Counter()
    covered = 0

    with tempfile.TemporaryDirectory(prefix="leetcode-reference-") as tmp:
        tmp_path = Path(tmp)
        kamyu = tmp_path / "LeetCode-Solutions"
        doocs = tmp_path / "doocs-leetcode"
        run("git", "clone", "--depth=1", "--filter=blob:none", KAMYU + ".git", str(kamyu))
        indexes = build_kamyu_indexes(kamyu)

        unresolved = []
        metadata_by_number = {}

        for number in range(START, END + 1):
            meta_path = PROBLEMS / str(number) / "metadata.json"
            if not meta_path.exists():
                missing_metadata.append(number)
                continue
            data = json.loads(meta_path.read_text(encoding="utf-8"))
            metadata_by_number[number] = data
            slug = data.get("slug") or data.get("url", "").rstrip("/").split("/")[-1]
            if not slug:
                unresolved.append(number)
                continue

            found_languages = []
            for language, index in indexes:
                if slug in index:
                    found_languages.append(language)
                    by_language[language] += 1

            if found_languages:
                covered += 1
                source_counts["kamyu104/LeetCode-Solutions"] += 1
            else:
                unresolved.append(number)

        if unresolved:
            clone_doocs_sparse(doocs)
            for number in unresolved:
                data = metadata_by_number.get(number)
                if data and doocs_has_solution(doocs, data):
                    covered += 1
                    source_counts["doocs/leetcode fallback"] += 1
                else:
                    missing_reference.append(number)

    lines = [
        "# Reference solution coverage",
        "",
        f"- Range: **{START}–{END}**",
        f"- Problems with at least one matching upstream solution: **{covered} / {END - START + 1}**",
        f"- Missing local metadata: **{len(missing_metadata)}**",
        f"- Missing upstream reference solution: **{len(missing_reference)}**",
        "",
        "## Reference source coverage",
        "",
    ]
    for source, count in source_counts.most_common():
        lines.append(f"- {source}: {count}")
    lines.extend(["", "## Kamyu matching files by language", ""])
    for language, count in by_language.most_common():
        lines.append(f"- {language}: {count}")
    lines.extend(["", "## Missing reference IDs", ""])
    lines.append(", ".join(map(str, missing_reference)) if missing_reference else "None")
    (ROOT / "REFERENCE_COVERAGE.md").write_text("\n".join(lines) + "\n", encoding="utf-8")

    if missing_metadata:
        print("Missing metadata IDs:", ", ".join(map(str, missing_metadata)))
    if missing_reference:
        print("Missing upstream reference IDs:", ", ".join(map(str, missing_reference)))

    if missing_metadata or missing_reference:
        raise SystemExit(
            f"Reference coverage failed: metadata_missing={len(missing_metadata)}, "
            f"reference_missing={len(missing_reference)}"
        )

    print(f"Reference coverage passed: {covered}/{END - START + 1} problems matched known solution sources.")
    for source, count in source_counts.most_common():
        print(f"  {source}: {count}")


if __name__ == "__main__":
    main()
