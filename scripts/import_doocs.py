#!/usr/bin/env python3
"""Import missing solution code for LeetCode 3000..4000 from doocs/leetcode.

Only solution code blocks and minimal metadata are imported. Full LeetCode problem
statements are deliberately not mirrored. Existing local solution files are kept.
Imported code is attributed to doocs/leetcode and remains under its CC BY-SA 4.0
license; see NOTICE.md.
"""
from __future__ import annotations

import json
import re
import subprocess
import tempfile
from pathlib import Path

from locked_sources import clone_locked

ROOT = Path(__file__).resolve().parents[1]
PROBLEMS = ROOT / "problems"
START, END = 3000, 4000
UPSTREAM = "https://github.com/doocs/leetcode"

LANGUAGES = {
    "Python3": ("python", "python.py"),
    "Python": ("python", "python.py"),
    "Java": ("java", "java.java"),
    "C++": ("cpp", "cpp.cpp"),
    "C": ("c", "c.c"),
    "C#": ("csharp", "csharp.cs"),
    "Go": ("go", "go.go"),
    "TypeScript": ("typescript", "typescript.ts"),
    "JavaScript": ("javascript", "javascript.js"),
    "Rust": ("rust", "rust.rs"),
    "Kotlin": ("kotlin", "kotlin.kt"),
    "Swift": ("swift", "swift.swift"),
    "Scala": ("scala", "scala.scala"),
    "Dart": ("dart", "dart.dart"),
    "Ruby": ("ruby", "ruby.rb"),
    "PHP": ("php", "php.php"),
    "Racket": ("racket", "racket.rkt"),
    "Erlang": ("erlang", "erlang.erl"),
    "Elixir": ("elixir", "elixir.ex"),
    "MySQL": ("mysql", "mysql.sql"),
    "PostgreSQL": ("postgresql", "postgresql.sql"),
    "Pandas": ("pandas", "pandas.py"),
}

TAB_RE = re.compile(
    r"^####\s+([^\n]+?)\s*\n+```[^\n]*\n(.*?)\n```",
    re.MULTILINE | re.DOTALL,
)
TITLE_RE = re.compile(r"^#\s+\[(\d+)\.\s*(.+?)(?:\s+🔒)?\]\(", re.MULTILINE)
DIFFICULTY_RE = re.compile(r"^difficulty:\s*(\w+)", re.MULTILINE)
LINK_RE = re.compile(r"^#\s+\[\d+\..+?\]\((https://leetcode\.com/problems/[^)]+)\)", re.MULTILINE)


def run(*args: str, cwd: Path | None = None) -> None:
    subprocess.run(args, cwd=cwd, check=True)


def clone_upstream(destination: Path) -> None:
    sparse = [f"solution/{start:04d}-{start + 99:04d}" for start in range(3000, 4100, 100)]
    clone_locked("doocs", destination, sparse)


def parse_problem(readme: Path) -> tuple[str | None, str | None, str | None, dict[str, str]]:
    text = readme.read_text(encoding="utf-8", errors="replace")
    title_match = TITLE_RE.search(text)
    difficulty_match = DIFFICULTY_RE.search(text)
    link_match = LINK_RE.search(text)
    title = title_match.group(2).strip() if title_match else None
    difficulty = difficulty_match.group(1) if difficulty_match else None
    url = link_match.group(1) if link_match else None

    snippets: dict[str, str] = {}
    for heading, code in TAB_RE.findall(text):
        heading = heading.strip()
        if heading not in LANGUAGES:
            continue
        code = code.strip()
        if not code:
            continue
        key, _ = LANGUAGES[heading]
        snippets.setdefault(key, code + "\n")
    return title, difficulty, url, snippets


def find_problem_dirs(upstream: Path):
    solution_root = upstream / "solution"
    for bucket in sorted(solution_root.iterdir()):
        if not bucket.is_dir():
            continue
        for directory in sorted(bucket.iterdir()):
            match = re.match(r"^(\d{4})\.", directory.name)
            if not match:
                continue
            number = int(match.group(1))
            if START <= number <= END:
                yield number, directory


def main() -> None:
    PROBLEMS.mkdir(exist_ok=True)
    imported_files = 0
    discovered = set()
    language_totals: dict[str, int] = {}

    with tempfile.TemporaryDirectory(prefix="leetcode-doocs-") as tmp:
        upstream = Path(tmp) / "leetcode"
        clone_upstream(upstream)

        for number, source_dir in find_problem_dirs(upstream):
            readme = source_dir / "README_EN.md"
            if not readme.exists():
                continue
            discovered.add(number)
            title, difficulty, url, snippets = parse_problem(readme)
            target = PROBLEMS / str(number)
            target.mkdir(parents=True, exist_ok=True)
            metadata_path = target / "metadata.json"
            if metadata_path.exists():
                try:
                    metadata = json.loads(metadata_path.read_text(encoding="utf-8"))
                except json.JSONDecodeError as exc:
                    raise ValueError(f"Refusing to overwrite invalid metadata: {metadata_path}") from exc
            else:
                metadata = {"number": number, "languages": {}}

            metadata.setdefault("number", number)
            if title:
                metadata.setdefault("title", title)
            if difficulty:
                metadata.setdefault("difficulty", difficulty)
            if url:
                metadata.setdefault("url", url)
                slug = url.rstrip("/").split("/")[-1]
                metadata.setdefault("slug", slug)
            metadata.setdefault("languages", {})
            metadata["upstream"] = {
                "repository": "doocs/leetcode",
                "path": str(source_dir.relative_to(upstream)).replace("\\", "/"),
                "license": "CC BY-SA 4.0",
                "url": f"{UPSTREAM}/tree/main/{str(source_dir.relative_to(upstream)).replace(chr(92), '/')}",
            }

            for language, code in snippets.items():
                filename = next(filename for key, filename in LANGUAGES.values() if key == language)
                output = target / filename
                if output.exists():
                    metadata["languages"].setdefault(language, "unverified")
                    continue
                output.write_text(code, encoding="utf-8")
                metadata["languages"][language] = "imported-unverified"
                imported_files += 1
                language_totals[language] = language_totals.get(language, 0) + 1

            statuses = set(metadata["languages"].values())
            if any(status == "verified" for status in statuses):
                metadata["status"] = "partially-verified"
            elif snippets:
                metadata["status"] = "unverified"
            else:
                metadata.setdefault("status", "missing")
            metadata_path.write_text(json.dumps(metadata, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    missing = [number for number in range(START, END + 1) if number not in discovered]
    lines = [
        "# Automated import status",
        "",
        f"- Numeric range: **{START}–{END}**",
        f"- Upstream problem directories discovered: **{len(discovered)} / {END - START + 1}**",
        f"- New solution files imported in this run: **{imported_files}**",
        f"- Numeric IDs not present in the upstream index: **{len(missing)}**",
        "",
        "## Imported files by language",
        "",
    ]
    for language, count in sorted(language_totals.items(), key=lambda item: (-item[1], item[0])):
        lines.append(f"- {language}: {count}")
    if missing:
        lines.extend(["", "## IDs not discovered upstream", "", ", ".join(map(str, missing))])
    lines.extend([
        "",
        "Imported snippets are not automatically labeled as LeetCode-verified. See `NOTICE.md` for attribution and licensing.",
    ])
    (ROOT / "IMPORT_STATUS.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
