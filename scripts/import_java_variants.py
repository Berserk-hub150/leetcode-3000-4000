#!/usr/bin/env python3
"""Add missing Java solutions from pinned MIT sources; never overwrite files."""
from __future__ import annotations

import argparse
import json
import re
import tempfile
from collections import Counter
from pathlib import Path

from locked_sources import clone_locked, get_sources

ROOT = Path(__file__).resolve().parents[1]


def transform_java(text: str, transform: str) -> str:
    text = text.replace("\r\n", "\n")
    if transform == "remove-java-package-public-v1":
        text = re.sub(r"^package [^;]+;\s*\n", "", text, count=1)
        text = re.sub(r"^public (class|final class|abstract class|interface|enum) ", r"\1 ", text, flags=re.MULTILINE)
    elif transform == "java-standard-imports-v1":
        text = "import java.util.*;\nimport java.util.stream.*;\nimport java.math.*;\n\n" + text
    else:
        raise ValueError(f"Unknown Java transformation: {transform}")
    return text.strip() + "\n"


def candidates(checkout: Path, source_id: str) -> dict[int, Path]:
    out = {}
    if source_id == "leetcode_java":
        for directory in sorted((checkout / "src/main/java").glob("*/s[34][0-9][0-9][0-9]_*")):
            number = int(directory.name[1:5])
            files = list(directory.glob("*.java"))
            if len(files) != 1:
                # Multi-file submissions need explicit review rather than an
                # arbitrary file selection.
                continue
            out[number] = files[0]
    elif source_id == "walkccc":
        for path in sorted((checkout / "solutions").glob("*/*.java")):
            if re.fullmatch(r"[34][0-9]{3}\.java", path.name):
                out[int(path.stem)] = path
    return out


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="Only list eligible additions")
    args = parser.parse_args()
    sources = get_sources()
    added = Counter()
    with tempfile.TemporaryDirectory(prefix="leetcode-java-import-") as temp:
        indexes = []
        for source_id, transform in [
            ("leetcode_java", "remove-java-package-public-v1"),
            ("walkccc", "java-standard-imports-v1"),
        ]:
            checkout = Path(temp) / source_id
            sparse = ["src/main/java"] if source_id == "leetcode_java" else ["solutions"]
            clone_locked(source_id, checkout, sparse)
            indexes.append((source_id, transform, checkout, candidates(checkout, source_id)))

        for number in range(3000, 4001):
            directory = ROOT / "problems" / str(number)
            output = directory / "java.java"
            if output.exists() or any(directory.glob("*.sql")):
                continue
            metadata_file = directory / "metadata.json"
            metadata = json.loads(metadata_file.read_text(encoding="utf-8"))
            for source_id, transform, checkout, index in indexes:
                source_file = index.get(number)
                if not source_file:
                    continue
                # IDs are the stable join key; make the title/path visible in
                # metadata so a reviewer can also confirm semantic identity.
                code = transform_java(source_file.read_text(encoding="utf-8"), transform)
                added[source_id] += 1
                if args.check:
                    print(f"{number}: {source_id}: {source_file.relative_to(checkout)}")
                    break
                output.write_text(code, encoding="utf-8")
                metadata.setdefault("languages", {})["java"] = "imported-unverified"
                metadata.setdefault("additional_sources", {})["java"] = {
                    "source": source_id,
                    "repository": sources[source_id]["repository"],
                    "commit": sources[source_id]["commit"],
                    "license": sources[source_id]["license"],
                    "path": str(source_file.relative_to(checkout)),
                    "transform": transform,
                }
                metadata["status"] = "partially-verified" if any(
                    value == "verified" for value in metadata["languages"].values()
                ) else "unverified"
                metadata_file.write_text(json.dumps(metadata, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
                break
    print(f"Java variants {'available' if args.check else 'added'}: {sum(added.values())}: {dict(added)}")


if __name__ == "__main__":
    main()
