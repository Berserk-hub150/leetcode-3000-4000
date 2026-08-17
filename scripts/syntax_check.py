#!/usr/bin/env python3
from __future__ import annotations

import sys
from collections import Counter
from pathlib import Path

from tree_sitter_language_pack import detect_language_from_path, get_parser

ROOT = Path(__file__).resolve().parents[1]
PROBLEMS = ROOT / "problems"
SOLUTION_SUFFIXES = {
    ".py", ".cpp", ".cc", ".cxx", ".c", ".java", ".go", ".rs", ".ts",
    ".js", ".cs", ".php", ".rb", ".swift", ".scala", ".dart", ".kt",
    ".rkt", ".erl", ".ex", ".sql",
}


def iter_error_nodes(node, limit: int = 3):
    found = []
    stack = [node]
    while stack and len(found) < limit:
        current = stack.pop()
        if current.type == "ERROR" or current.is_missing:
            found.append(current)
        stack.extend(reversed(current.children))
    return found


def main() -> None:
    files = sorted(
        p for p in PROBLEMS.glob("*/*")
        if p.is_file() and p.suffix.lower() in SOLUTION_SUFFIXES
    )
    if not files:
        print("ERROR: no solution files found", file=sys.stderr)
        raise SystemExit(1)

    parsers = {}
    counts = Counter()
    failures = []
    unsupported = []

    for path in files:
        language = detect_language_from_path(str(path))
        if not language:
            unsupported.append(str(path.relative_to(ROOT)))
            continue
        try:
            parser = parsers.setdefault(language, get_parser(language))
        except Exception as exc:
            failures.append((path, language, f"parser setup failed: {exc}"))
            continue

        source = path.read_bytes()
        tree = parser.parse(source)
        if tree is None:
            failures.append((path, language, "parser returned no syntax tree"))
            continue

        counts[language] += 1
        root = tree.root_node
        if root.has_error:
            details = []
            for node in iter_error_nodes(root):
                row, col = node.start_point
                details.append(f"{node.type}@{row + 1}:{col + 1}")
            failures.append((path, language, ", ".join(details) or "syntax error"))

    print(f"Parsed {sum(counts.values())} solution files across {len(counts)} grammars.")
    for language, count in sorted(counts.items(), key=lambda item: (-item[1], item[0])):
        print(f"  {language}: {count}")

    if unsupported:
        print("ERROR: unsupported solution file extensions:", file=sys.stderr)
        for path in unsupported[:50]:
            print(f"  {path}", file=sys.stderr)
        raise SystemExit(1)

    if failures:
        print(f"ERROR: {len(failures)} files contain parser errors:", file=sys.stderr)
        for path, language, detail in failures[:200]:
            print(f"  {path.relative_to(ROOT)} [{language}]: {detail}", file=sys.stderr)
        if len(failures) > 200:
            print(f"  ... and {len(failures) - 200} more", file=sys.stderr)
        raise SystemExit(1)

    print("All solution files passed language-aware syntax parsing.")


if __name__ == "__main__":
    main()
