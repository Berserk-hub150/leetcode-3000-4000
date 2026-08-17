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
KAMYU_REPO = "kamyu104/LeetCode-Solutions"
KAMYU_URL = "https://github.com/kamyu104/LeetCode-Solutions"
DOOCS_URL = "https://github.com/doocs/leetcode"

# local language -> local filename
LOCAL_FILES = {
    "python": "python.py", "python3": "python.py", "java": "java.java", "cpp": "cpp.cpp",
    "c": "c.c", "csharp": "csharp.cs", "go": "go.go", "typescript": "typescript.ts",
    "javascript": "javascript.js", "rust": "rust.rs", "kotlin": "kotlin.kt",
    "swift": "swift.swift", "scala": "scala.scala", "dart": "dart.dart", "ruby": "ruby.rb",
    "php": "php.php", "racket": "racket.rkt", "erlang": "erlang.erl", "elixir": "elixir.ex",
    "mysql": "mysql.sql", "postgresql": "postgresql.sql", "pandas": "pandas.py",
}

KAMYU_SOURCES = [
    ("Python3", ".py", "python", "python.py"),
    ("Python", ".py", "python", "python.py"),
    ("C++", ".cpp", "cpp", "cpp.cpp"),
    ("Java", ".java", "java", "java.java"),
    ("Golang", ".go", "go", "go.go"),
    ("C#", ".cs", "csharp", "csharp.cs"),
    ("Kotlin", ".kt", "kotlin", "kotlin.kt"),
    ("MySQL", ".sql", "mysql", "mysql.sql"),
    ("PHP", ".php", "php", "php.php"),
    ("Pandas", ".py", "pandas", "pandas.py"),
]

DOOCS_HEADINGS = {
    "Python3": "python", "Python": "python", "Java": "java", "C++": "cpp", "C": "c",
    "C#": "csharp", "Go": "go", "TypeScript": "typescript", "JavaScript": "javascript",
    "Rust": "rust", "Kotlin": "kotlin", "Swift": "swift", "Scala": "scala", "Dart": "dart",
    "Ruby": "ruby", "PHP": "php", "Racket": "racket", "Erlang": "erlang", "Elixir": "elixir",
    "MySQL": "mysql", "PostgreSQL": "postgresql", "Pandas": "pandas",
}
TAB_RE = re.compile(r"^####\s+([^\n]+?)\s*\n+```[^\n]*\n(.*?)\n```", re.MULTILINE | re.DOTALL)


def run(*args: str, cwd: Path | None = None) -> None:
    subprocess.run(args, cwd=cwd, check=True, stdout=subprocess.DEVNULL)


def normalize(text: str) -> str:
    return text.replace("\r\n", "\n").replace("\r", "\n").strip() + "\n"


def build_kamyu_indexes(upstream: Path):
    indexes: dict[str, dict[str, Path]] = {}
    for dirname, extension, language, _ in KAMYU_SOURCES:
        root = upstream / dirname
        index = indexes.setdefault(language, {})
        if root.exists():
            for path in root.rglob(f"*{extension}"):
                index.setdefault(path.stem, path)
    return indexes


def clone_doocs(destination: Path) -> None:
    run("git", "clone", "--depth=1", "--filter=blob:none", "--sparse", DOOCS_URL + ".git", str(destination))
    buckets = [f"solution/{start:04d}-{start + 99:04d}" for start in range(3000, 4100, 100)]
    run("git", "sparse-checkout", "set", *buckets, cwd=destination)


def parse_doocs(readme: Path) -> dict[str, str]:
    if not readme.exists():
        return {}
    text = readme.read_text(encoding="utf-8", errors="replace")
    out: dict[str, str] = {}
    for heading, code in TAB_RE.findall(text):
        language = DOOCS_HEADINGS.get(heading.strip())
        if language and code.strip():
            out.setdefault(language, normalize(code))
    return out


def main() -> None:
    replaced = Counter()
    matched = Counter()
    no_reference = Counter()
    touched_problems = set()

    with tempfile.TemporaryDirectory(prefix="leetcode-source-back-") as tmp:
        tmp_path = Path(tmp)
        kamyu = tmp_path / "kamyu"
        doocs = tmp_path / "doocs"
        run("git", "clone", "--depth=1", "--filter=blob:none", KAMYU_URL + ".git", str(kamyu))
        clone_doocs(doocs)
        kamyu_indexes = build_kamyu_indexes(kamyu)

        for number in range(3000, 4001):
            problem = PROBLEMS / str(number)
            meta_path = problem / "metadata.json"
            if not meta_path.exists():
                continue
            data = json.loads(meta_path.read_text(encoding="utf-8"))
            slug = data.get("slug") or data.get("url", "").rstrip("/").split("/")[-1]
            if not slug:
                continue

            primary = data.get("upstream") or {}
            doocs_snippets = {}
            if primary.get("repository") == "doocs/leetcode" and primary.get("path"):
                doocs_snippets = parse_doocs(doocs / primary["path"] / "README_EN.md")

            secondary = data.get("secondary_upstream")
            if not isinstance(secondary, dict) or secondary.get("repository") != KAMYU_REPO:
                secondary = {
                    "repository": KAMYU_REPO,
                    "url": KAMYU_URL,
                    "license": "MIT",
                    "copyright": "Copyright (c) 2018 https://github.com/kamyu104/LeetCode-Solutions",
                    "files": {},
                }
            secondary.setdefault("files", {})

            changed = False
            statuses = data.setdefault("languages", {})
            # Work from actual files as well as metadata aliases.
            candidate_languages = set(statuses)
            for language, filename in LOCAL_FILES.items():
                if (problem / filename).exists():
                    candidate_languages.add(language)

            processed_files = set()
            for language in sorted(candidate_languages):
                normalized_language = "python" if language == "python3" else language
                filename = LOCAL_FILES.get(language) or LOCAL_FILES.get(normalized_language)
                if not filename or filename in processed_files:
                    continue
                local = problem / filename
                if not local.exists():
                    continue
                processed_files.add(filename)

                # Already source-backed and integrity-checked elsewhere.
                existing_status = statuses.get(normalized_language) or statuses.get(language)
                if existing_status == "imported-unverified":
                    continue

                source_text = None
                source_kind = None
                source_relative = None

                kamyu_source = kamyu_indexes.get(normalized_language, {}).get(slug)
                if kamyu_source is not None:
                    source_text = normalize(kamyu_source.read_text(encoding="utf-8", errors="replace"))
                    source_kind = "kamyu"
                    source_relative = str(kamyu_source.relative_to(kamyu)).replace("\\", "/")
                elif normalized_language in doocs_snippets:
                    source_text = doocs_snippets[normalized_language]
                    source_kind = "doocs"

                if source_text is None:
                    no_reference[normalized_language] += 1
                    continue

                local_text = normalize(local.read_text(encoding="utf-8", errors="replace"))
                if local_text != source_text:
                    local.write_text(source_text, encoding="utf-8")
                    replaced[source_kind] += 1
                    changed = True
                else:
                    matched[source_kind] += 1

                statuses[normalized_language] = "imported-unverified"
                if language != normalized_language:
                    statuses.pop(language, None)
                if source_kind == "kamyu" and source_relative:
                    secondary["files"][normalized_language] = source_relative
                    data["secondary_upstream"] = secondary
                touched_problems.add(number)
                changed = True

            if changed:
                if any(v == "verified" for v in statuses.values()):
                    data["status"] = "partially-verified"
                else:
                    data["status"] = "unverified"
                meta_path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    report = [
        "# Source-backing pass",
        "",
        f"- Problems touched: **{len(touched_problems)}**",
        f"- Local files replaced by exact current reference implementations: **{sum(replaced.values())}**",
        f"- Local files already identical to a current reference: **{sum(matched.values())}**",
        f"- Local files with no same-language reference in the configured sources: **{sum(no_reference.values())}**",
        "",
        "## Replaced by source",
        "",
    ]
    for source, count in replaced.most_common():
        report.append(f"- {source}: {count}")
    report.extend(["", "## Already matched", ""])
    for source, count in matched.most_common():
        report.append(f"- {source}: {count}")
    report.extend(["", "## No configured same-language reference", ""])
    for language, count in no_reference.most_common():
        report.append(f"- {language}: {count}")
    (ROOT / "SOURCE_BACKING.md").write_text("\n".join(report) + "\n", encoding="utf-8")

    print(f"Source-backing complete: replaced={sum(replaced.values())}, already_matched={sum(matched.values())}, no_reference={sum(no_reference.values())}")


if __name__ == "__main__":
    main()
