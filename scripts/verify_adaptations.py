#!/usr/bin/env python3
"""Check the provenance and test coverage of deliberately non-identical adaptations."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

from locked_sources import get_sources
from test_java_translations import IDS

ROOT = Path(__file__).resolve().parents[1]


def main() -> None:
    sources = get_sources()
    numbers = set()
    for path in (ROOT / "problems").glob("*/metadata.json"):
        metadata = json.loads(path.read_text())
        for language, record in metadata.get("adapted_sources", {}).items():
            if language != "java" or record["base_language"] != "cpp" or record["base_file"] != "cpp.cpp":
                raise ValueError(f"Unsupported adaptation: {path}/{language}")
            if metadata["languages"].get(language) != "translated-unverified":
                raise ValueError(f"Adaptation must not claim source identity or judge acceptance: {path}")
            source = sources[record["source"]]
            for key in ("repository", "commit", "license"):
                if record[key] != source[key]:
                    raise ValueError(f"Adaptation source differs from lock: {path}/{key}")
            secondary = metadata.get("secondary_upstream", {}).get("files", {}).get("cpp")
            expected_source = "kamyu" if secondary else "doocs"
            expected_path = secondary or metadata["upstream"]["path"] + "/README_EN.md"
            if record["source"] != expected_source or record["path"] != expected_path:
                raise ValueError(f"Adaptation does not name its C++ source: {path}")
            digest = hashlib.sha256((path.parent / "cpp.cpp").read_bytes()).hexdigest()
            if digest != record["base_sha256"]:
                raise ValueError(f"C++ adaptation base changed; review Java and tests: {path}")
            java = (path.parent / "java.java").read_text()
            spdx = "MIT" if expected_source == "kamyu" else "CC-BY-SA-4.0"
            if f"SPDX-License-Identifier: {spdx}" not in java or record["commit"] not in java:
                raise ValueError(f"Missing adaptation license/source header: {path}")
            numbers.add(metadata["number"])
    if numbers != set(IDS):
        raise ValueError(f"Adaptations and regression-test manifest differ: {numbers ^ set(IDS)}")
    print(f"Adaptation provenance: {len(numbers)}/{len(IDS)} recorded with regression coverage")


if __name__ == "__main__":
    main()
