#!/usr/bin/env python3
"""Reconstruct added Java imports from immutable, attributed source commits."""
from __future__ import annotations

import json
import tempfile
from pathlib import Path

from import_java_variants import transform_java
from locked_sources import clone_locked, get_sources, safe_source_path

ROOT = Path(__file__).resolve().parents[1]


def main() -> None:
    sources = get_sources()
    records = []
    for metadata_path in sorted((ROOT / "problems").glob("*/metadata.json")):
        data = json.loads(metadata_path.read_text(encoding="utf-8"))
        for language, record in data.get("additional_sources", {}).items():
            records.append((metadata_path.parent, language, record))
    checked = 0
    with tempfile.TemporaryDirectory(prefix="leetcode-added-integrity-") as tmp:
        checkouts = {}
        for source_id in sorted({r[2]["source"] for r in records}):
            checkout = Path(tmp) / source_id
            clone_locked(source_id, checkout)
            checkouts[source_id] = checkout
        for directory, language, record in records:
            source_id = record["source"]
            locked = sources[source_id]
            for key in ("repository", "commit", "license"):
                if record.get(key) != locked[key]:
                    raise ValueError(f"{directory.name}/{language}: {key} differs from source lock")
            if language != "java":
                raise ValueError(f"Unsupported additional language: {language}")
            source = safe_source_path(checkouts[source_id], record["path"])
            expected = transform_java(source.read_text(encoding="utf-8"), record["transform"])
            actual = (directory / "java.java").read_text(encoding="utf-8")
            if expected != actual:
                raise ValueError(f"{directory.name}/{language}: differs from pinned source transformation")
            checked += 1
    print(f"Additional source integrity: {checked}/{len(records)} matched")


if __name__ == "__main__":
    main()
