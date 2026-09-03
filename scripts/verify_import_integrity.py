#!/usr/bin/env python3
from __future__ import annotations

import json
import re
import subprocess
import tempfile
from collections import Counter
from pathlib import Path

from locked_sources import clone_locked
from source_patches import apply_source_patches

ROOT = Path(__file__).resolve().parents[1]
PROBLEMS = ROOT / "problems"
DOOCS = "https://github.com/doocs/leetcode"
KAMYU = "https://github.com/kamyu104/LeetCode-Solutions"

LOCAL_FILES = {
    "python": "python.py",
    "java": "java.java",
    "cpp": "cpp.cpp",
    "c": "c.c",
    "csharp": "csharp.cs",
    "go": "go.go",
    "typescript": "typescript.ts",
    "javascript": "javascript.js",
    "rust": "rust.rs",
    "kotlin": "kotlin.kt",
    "swift": "swift.swift",
    "scala": "scala.scala",
    "dart": "dart.dart",
    "ruby": "ruby.rb",
    "php": "php.php",
    "racket": "racket.rkt",
    "erlang": "erlang.erl",
    "elixir": "elixir.ex",
    "mysql": "mysql.sql",
    "postgresql": "postgresql.sql",
    "pandas": "pandas.py",
}

DOOCS_HEADINGS = {
    "Python3": "python", "Python": "python", "Java": "java", "C++": "cpp",
    "C": "c", "C#": "csharp", "Go": "go", "TypeScript": "typescript",
    "JavaScript": "javascript", "Rust": "rust", "Kotlin": "kotlin",
    "Swift": "swift", "Scala": "scala", "Dart": "dart", "Ruby": "ruby",
    "PHP": "php", "Racket": "racket", "Erlang": "erlang", "Elixir": "elixir",
    "MySQL": "mysql", "PostgreSQL": "postgresql", "Pandas": "pandas",
}
TAB_RE = re.compile(
    r"^####\s+([^\n]+?)\s*\n+```[^\n]*\n(.*?)\n```",
    re.MULTILINE | re.DOTALL,
)


def run(*args: str, cwd: Path | None = None) -> None:
    subprocess.run(args, cwd=cwd, check=True, stdout=subprocess.DEVNULL)


def clone_doocs(destination: Path) -> None:
    buckets = [f"solution/{start:04d}-{start + 99:04d}" for start in range(3000, 4100, 100)]
    clone_locked("doocs", destination, buckets)


def normalize_text(text: str) -> str:
    return text.replace("\r\n", "\n").replace("\r", "\n").strip() + "\n"


def parse_doocs(readme: Path) -> dict[str, str]:
    text = readme.read_text(encoding="utf-8", errors="replace")
    snippets: dict[str, str] = {}
    for heading, code in TAB_RE.findall(text):
        language = DOOCS_HEADINGS.get(heading.strip())
        if not language or not code.strip():
            continue
        snippets.setdefault(language, normalize_text(code))
    return snippets


def main() -> None:
    checked = Counter()
    failures: list[str] = []
    skipped = Counter()

    with tempfile.TemporaryDirectory(prefix="leetcode-integrity-") as tmp:
        tmp_path = Path(tmp)
        doocs = tmp_path / "doocs"
        kamyu = tmp_path / "kamyu"
        clone_doocs(doocs)
        clone_locked("kamyu", kamyu)

        for number in range(3000, 4001):
            problem = PROBLEMS / str(number)
            metadata_path = problem / "metadata.json"
            if not metadata_path.exists():
                failures.append(f"{number}: missing metadata")
                continue
            data = json.loads(metadata_path.read_text(encoding="utf-8"))
            language_statuses = data.get("languages", {})
            secondary = data.get("secondary_upstream") or {}
            secondary_files = secondary.get("files", {}) if secondary.get("repository") == "kamyu104/LeetCode-Solutions" else {}

            doocs_snippets: dict[str, str] | None = None
            primary = data.get("upstream") or {}
            if primary.get("repository") == "doocs/leetcode" and primary.get("path"):
                readme = doocs / primary["path"] / "README_EN.md"
                if readme.exists():
                    doocs_snippets = parse_doocs(readme)

            for language, status in language_statuses.items():
                if language in data.get("additional_sources", {}):
                    continue  # Checked by verify_additional_sources.py.
                if status != "imported-unverified":
                    skipped[status] += 1
                    continue

                local_name = LOCAL_FILES.get(language)
                if not local_name:
                    failures.append(f"{number}/{language}: no local filename mapping")
                    continue
                local = problem / local_name
                if not local.exists():
                    failures.append(f"{number}/{language}: metadata says imported but {local_name} is missing")
                    continue
                local_text = normalize_text(local.read_text(encoding="utf-8", errors="replace"))

                # Prefer the explicitly recorded secondary source for this language.
                kamyu_relative = secondary_files.get(language)
                if kamyu_relative:
                    source = kamyu / kamyu_relative
                    if not source.exists():
                        failures.append(f"{number}/{language}: recorded Kamyu source missing: {kamyu_relative}")
                        continue
                    source_text = normalize_text(source.read_text(encoding="utf-8", errors="replace"))
                    source_text = apply_source_patches(source_text, number, language,
                                                       data.get("source_patches", {}).get(language, []))
                    if local_text != source_text:
                        failures.append(f"{number}/{language}: differs from recorded Kamyu source {kamyu_relative}")
                    else:
                        checked["kamyu"] += 1
                    continue

                if doocs_snippets and language in doocs_snippets:
                    expected = apply_source_patches(doocs_snippets[language], number, language,
                                                    data.get("source_patches", {}).get(language, []))
                    if local_text != expected:
                        failures.append(f"{number}/{language}: differs from pinned Doocs {language} snippet and declared patches")
                    else:
                        checked["doocs"] += 1
                    continue

                failures.append(f"{number}/{language}: imported source cannot be reconstructed")

    total = sum(checked.values())
    print(f"Imported solution integrity checked: {total} files")
    for source, count in checked.most_common():
        print(f"  {source}: {count}")

    if failures:
        print(f"ERROR: {len(failures)} import-integrity failures")
        for item in failures[:250]:
            print("  " + item)
        if len(failures) > 250:
            print(f"  ... and {len(failures) - 250} more")
        raise SystemExit(1)

    print("All imported files match their pinned source plus any explicitly recorded local patches.")


if __name__ == "__main__":
    main()
