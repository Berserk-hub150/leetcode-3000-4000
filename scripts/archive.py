"""Shared canonical file inventory used by validation and generated documents."""
from __future__ import annotations

import json
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def inventory(root: Path = ROOT) -> tuple[dict[str, str], list[dict]]:
    languages = json.loads((root / "languages.json").read_text(encoding="utf-8"))
    if len(set(languages.values())) != len(languages):
        raise ValueError("Canonical filenames must be unique")
    problems = []
    for metadata_path in sorted((root / "problems").glob("*/metadata.json"), key=lambda p: int(p.parent.name)):
        metadata = json.loads(metadata_path.read_text(encoding="utf-8"))
        files = {language: filename for language, filename in languages.items()
                 if (metadata_path.parent / filename).is_file() and (metadata_path.parent / filename).stat().st_size > 0}
        problems.append({"metadata": metadata, "files": files,
                         "database": any(name.endswith(".sql") for name in files.values())})
    return languages, problems


def statistics(problems: list[dict]) -> dict:
    counts = Counter()
    statuses = Counter()
    for problem in problems:
        counts.update(problem["files"].keys())
        for language in problem["files"]:
            statuses[problem["metadata"].get("languages", {}).get(language, "unrecorded")] += 1
    return {"covered": sum(bool(p["files"]) for p in problems), "files": sum(counts.values()),
            "languages": counts, "statuses": statuses,
            "database": sum(p["database"] for p in problems),
            "algorithms": sum(not p["database"] for p in problems)}
