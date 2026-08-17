#!/usr/bin/env python3
import json
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PROBLEMS = ROOT / "problems"
START, END = 3000, 4000

solution_suffixes = {
    ".py", ".cpp", ".java", ".go", ".ts", ".js", ".rs", ".cs", ".c",
    ".kt", ".swift", ".scala", ".dart", ".rb", ".php", ".rkt", ".erl",
    ".ex", ".sql",
}
ignore_names = {"metadata.json", "README.md"}

solved = []
missing = []
file_count = 0
languages = Counter()
status_counts = Counter()

for number in range(START, END + 1):
    directory = PROBLEMS / str(number)
    files = []
    if directory.exists():
        for path in directory.iterdir():
            if path.is_file() and path.name not in ignore_names and path.suffix.lower() in solution_suffixes:
                files.append(path)
    if files:
        solved.append(number)
        file_count += len(files)
        for path in files:
            languages[path.suffix.lower()] += 1
    else:
        missing.append(number)

    metadata_path = directory / "metadata.json"
    if metadata_path.exists():
        try:
            metadata = json.loads(metadata_path.read_text(encoding="utf-8"))
            status_counts[metadata.get("status", "unknown")] += 1
        except Exception:
            status_counts["invalid-metadata"] += 1

lines = [
    "# Coverage report",
    "",
    f"- Range: **{START}–{END}**",
    f"- Problems with at least one solution file: **{len(solved)} / {END - START + 1}**",
    f"- Problems with no solution file: **{len(missing)}**",
    f"- Total solution files currently present: **{file_count}**",
    "",
    "## Files by extension",
    "",
]
for extension, count in languages.most_common():
    lines.append(f"- `{extension}`: {count}")
lines.extend(["", "## Metadata status counts", ""])
for status, count in status_counts.most_common():
    lines.append(f"- `{status}`: {count}")
lines.extend(["", "## Missing solution IDs", ""])
lines.append(", ".join(map(str, missing)) if missing else "None — every ID in the range has at least one solution file.")
lines.append("")
(ROOT / "COVERAGE.md").write_text("\n".join(lines), encoding="utf-8")
