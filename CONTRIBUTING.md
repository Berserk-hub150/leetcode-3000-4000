# Contributing

Add or improve one real implementation for LeetCode problems 3000–4000 per pull
request. Do not add placeholders or copy full problem statements.

## Files and metadata

Canonical filenames are defined in [languages.json](languages.json): for example,
C++ uses cpp.cpp, Java uses java.java, and Python uses python.py.
Use the canonical metadata key python (not a second python3 alias).

Every declared language must have its corresponding non-empty file. Record the
problem number, title, slug, official URL, difficulty and language status.
SQL/database problems use their supported SQL/Pandas languages; C++ and Java
are not valid judge submissions for those problems.

## Verification statuses

- unverified: original implementation, without a recorded judge verification.
- imported-unverified: attributed upstream implementation, integrity-checked
  separately; this is not a claim of a LeetCode Accepted submission.
- translated-unverified: an adaptation with explicit per-language provenance,
  compilation and regression tests, without an authenticated judge result.
- verified: the exact implementation and current judge contract were checked;
  describe the evidence in the pull request.
- partially-verified: problem-level aggregate when language statuses differ.

Compilation, syntax parsing, source integrity and behavioral tests are different
checks. Do not advertise one as proof of another or claim all judge tests passed
unless that actually happened.

## Attribution and licensing

Read [LICENSE_SCOPE.md](LICENSE_SCOPE.md) before adding third-party code. Keep
the upstream copyright and full license notice, record the immutable source
commit in sources.lock.json, and record the per-file source path and any
transformation in metadata. Do not relicense CC BY-SA code as MIT.

## Local checks

Run these from the repository root with Python 3.12:

```sh
python scripts/validate.py
python scripts/generate_index.py --check
python scripts/report_coverage.py --check
python -m unittest discover -s tests
python scripts/verify_adaptations.py
python scripts/compile_java.py --new-only
python scripts/test_java_translations.py
```

Language parsing requires the pinned dependencies in the validation workflow.
Java compilation requires JDK 17 or later; differential tests also require a
C++20 compiler (`g++`). They execute the first C++ Solution class in isolation;
alternative C++ classes in the same upstream file are not covered by that test.
Source-integrity checks fetch only the revisions in sources.lock.json. Updating
a source revision and its affected implementations must be an explicit reviewed
change. Maintenance workflows that write to the repository are manual only.
