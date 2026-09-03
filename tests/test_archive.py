import json
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from archive import inventory, statistics
from generate_index import render
from import_java_variants import transform_java
from locked_sources import get_sources, safe_source_path
from source_patches import PATCHES, apply_source_patches
from test_java_translations import IDS, cases, oracle


class ArchiveTests(unittest.TestCase):
    def test_complete_inventory(self):
        _, problems = inventory()
        stats = statistics(problems)
        self.assertEqual(stats["covered"], 1001)
        self.assertEqual(stats["algorithms"], 927)
        self.assertEqual(stats["database"], 74)
        self.assertEqual(stats["languages"]["cpp"], 927)
        self.assertEqual(stats["languages"]["java"], 927)

    def test_imported_unverified_counts_and_links(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "languages.json").write_text(json.dumps({"java": "java.java"}))
            problem = root / "problems/3000"
            problem.mkdir(parents=True)
            (problem / "java.java").write_text("class Solution {}\n")
            (problem / "metadata.json").write_text(json.dumps({"number": 3000, "title": "Example", "languages": {"java": "imported-unverified"}}))
            _, rows = inventory(root)
            self.assertEqual(statistics(rows)["files"], 1)
            self.assertIn("problems/3000/java.java", render(root))

    def test_canonical_names(self):
        names, _ = inventory()
        self.assertEqual(names["cpp"], "cpp.cpp")
        self.assertEqual(names["java"], "java.java")
        self.assertEqual(names["csharp"], "csharp.cs")

    def test_source_lock_full_shas(self):
        for source in get_sources().values():
            self.assertRegex(source["commit"], r"^[0-9a-f]{40}$")

    def test_source_path_cannot_escape(self):
        with tempfile.TemporaryDirectory() as tmp:
            with self.assertRaises(ValueError):
                safe_source_path(Path(tmp), "../outside")

    def test_java_package_transform(self):
        source = "package example;\n\nimport java.util.*;\npublic class Solution {}\n"
        self.assertEqual(transform_java(source, "remove-java-package-public-v1"), "import java.util.*;\nclass Solution {}\n")

    def test_unknown_transform_rejected(self):
        with self.assertRaises(ValueError):
            transform_java("class Solution {}", "unknown")

    def test_patches_restricted_to_target(self):
        for name, (number, language, before, after) in PATCHES.items():
            self.assertEqual(apply_source_patches(before, number, language, [name]), after)
            with self.assertRaises(ValueError):
                apply_source_patches(before, 3000, language, [name])
            with self.assertRaises(ValueError):
                apply_source_patches(before + before, number, language, [name])

    def test_translation_cases_deterministic(self):
        self.assertEqual(len(IDS), 48)
        for number in IDS:
            self.assertEqual(cases(number, 2), cases(number, 2))

    def test_empty_rectangle_regression_oracle(self):
        self.assertEqual(oracle(3933, [[[1]]]), 1)
        self.assertEqual(oracle(3933, [[[1, 1], [1, 1]]]), 4)
        self.assertEqual(oracle(3933, [[[1, 2], [3, 4]]]), 1)

    def test_no_automatic_write_workflows(self):
        for path in (ROOT / ".github/workflows").glob("*.yml"):
            source = path.read_text()
            if "contents: write" in source:
                self.assertIn("  workflow_dispatch:", source, str(path))
                self.assertNotRegex(source, r"(?m)^  (push|pull_request|schedule|workflow_run):")
        self.assertIn("contents: read", (ROOT / ".github/workflows/validate.yml").read_text())


if __name__ == "__main__":
    unittest.main()
