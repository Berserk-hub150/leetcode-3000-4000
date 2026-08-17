#!/usr/bin/env python3
from __future__ import annotations

import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PROBLEMS = ROOT / "problems"

# Legacy names used by the initial bootstrap -> canonical archive filename.
RENAMES = {
    "solution.py": "python.py",
    "Solution.py": "python.py",
    "solution.cpp": "cpp.cpp",
    "Solution.cpp": "cpp.cpp",
    "solution.c": "c.c",
    "Solution.c": "c.c",
    "Solution.java": "java.java",
    "solution.java": "java.java",
    "Solution.cs": "csharp.cs",
    "solution.cs": "csharp.cs",
    "solution.js": "javascript.js",
    "Solution.js": "javascript.js",
    "solution.ts": "typescript.ts",
    "Solution.ts": "typescript.ts",
    "solution.go": "go.go",
    "Solution.go": "go.go",
    "solution.rs": "rust.rs",
    "Solution.rs": "rust.rs",
    "Solution.kt": "kotlin.kt",
    "solution.kt": "kotlin.kt",
    "Solution.swift": "swift.swift",
    "solution.swift": "swift.swift",
    "solution.rb": "ruby.rb",
    "Solution.rb": "ruby.rb",
    "solution.php": "php.php",
    "Solution.php": "php.php",
    "Solution.scala": "scala.scala",
    "solution.scala": "scala.scala",
    "solution.dart": "dart.dart",
    "Solution.dart": "dart.dart",
    "solution.rkt": "racket.rkt",
    "Solution.rkt": "racket.rkt",
    "solution.erl": "erlang.erl",
    "Solution.erl": "erlang.erl",
    "solution.ex": "elixir.ex",
    "Solution.ex": "elixir.ex",
}


def main() -> None:
    duplicates_removed = 0
    renamed = 0
    actions = []

    for problem in sorted(PROBLEMS.iterdir()):
        if not problem.is_dir():
            continue
        for legacy_name, canonical_name in RENAMES.items():
            legacy = problem / legacy_name
            if not legacy.exists():
                continue
            canonical = problem / canonical_name
            if canonical.exists():
                legacy.unlink()
                duplicates_removed += 1
                actions.append(f"{problem.name}: removed duplicate {legacy_name} (kept {canonical_name})")
            else:
                shutil.move(str(legacy), str(canonical))
                renamed += 1
                actions.append(f"{problem.name}: renamed {legacy_name} -> {canonical_name}")

    lines = [
        "# Filename normalization",
        "",
        f"- Legacy duplicate files removed: **{duplicates_removed}**",
        f"- Legacy-only files renamed to canonical names: **{renamed}**",
        "",
        "No language variant is intentionally removed: a legacy file is deleted only when the canonical file for the same language already exists.",
        "",
        "## Actions",
        "",
    ]
    lines.extend(f"- {action}" for action in actions)
    (ROOT / "FILENAME_NORMALIZATION.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"Filename normalization: removed_duplicates={duplicates_removed}, renamed={renamed}")


if __name__ == "__main__":
    main()
