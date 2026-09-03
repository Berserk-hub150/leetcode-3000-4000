# Verification scope

The archive contains 1,001 covered problem IDs and 4,659 canonical files.
C++ and Java each cover all 927 algorithm problems. The 74 SQL/database problems
are explicitly excluded from native C++/Java coverage, not filled with placeholders.

## File groups and reproducible checks

| Group | Files | Check |
|---|---:|---|
| Original doocs/Kamyu source-backed implementations | 4,419 | `verify_import_integrity.py`, pinned source reconstruction with explicitly recorded patches |
| Added MIT Java imports | 134 | `verify_additional_sources.py`, exact declared source transformations |
| Added Java adaptations | 48 | `verify_adaptations.py`, isolated compilation, `test_java_translations.py` |
| Existing residual language variants | 58 | Existing `verify_extra_variants.py` multi-runtime behavioral suite |
| Total | 4,659 | These groups are disjoint |

All source revisions are fixed in `sources.lock.json`; verification does not
compare against a moving upstream branch. Of the original 4,419 source-backed
files, 3,993 derive from doocs and 426 from Kamyu. Two Kamyu C++ files are now
reconstructed with reviewed local patches instead of being called byte-identical:

- **3933:** own the computed bounds to avoid dangling references; handle empty
  sparse-table rectangles before computing logarithms.
- **3953:** copy the maximum value instead of binding a reference to a temporary.

The exact transformations are restricted by problem/language in
`scripts/source_patches.py` and identified in the corresponding metadata.
Four doocs Java files (3625, 3709, 3748, 3822) also have recorded JDK 17 compatibility
patches: unused lambda names and last-element access. Their source license remains
CC BY-SA 4.0; the changes do not alter the algorithm.

## Java additions

134 imports retain their source path, license, immutable commit and transformation.
48 adaptations retain their C++ base hash, source path, license and change notice.
47 adaptations are MIT-derived; problem 3930 is CC BY-SA 4.0-derived.

The deterministic regression suite uses 48 generated small-input cases per
adaptation (2,304 cases). It compares the Java result with the first C++ Solution
class in isolation. For selected problems it additionally uses independent
brute-force or direct oracles. Seeds, generators and oracles are committed; failures
include the problem, input and mismatching outputs. Set `LEETCODE_CPP_SANITIZERS=1`
to enable address/undefined-behavior sanitizers for the C++ test executable.

These tests do not exhaust the input space or certify performance at every limit.
Compilation uses judge-like helper definitions where required, not the actual
authenticated LeetCode harness. Alternative C++ classes in an upstream file are
not covered by the differential suite. Hash-based solutions retain collision risk.

## Other checks

- `validate.py`: all 1,001 IDs, known statuses, canonical non-empty files,
  metadata/file agreement, mandatory C++ and Java for algorithm tasks.
- `generate_index.py --check` and `report_coverage.py --check`: documentation
  must match the complete inventory, including imported-unverified files.
- `syntax_check.py`: grammar parsing for every file and SQL dialect handling.
- `verify_reference_coverage.py`: a known reference for every problem slug.
- `compile_java.py`: isolated Java compilation; `--new-only` selects all 182 additions.
- `python -m unittest discover -s tests`: inventory, licensing transformations,
  source path safety, deterministic test data and workflow write restrictions.

The existing 58-variant report in `EXTRA_VARIANT_VERIFICATION.md` records earlier
runtime evidence. Its workflow re-executes those checks on affected changes; an
old successful run must not be treated as proof for a new commit. Check the
current commit's Actions results before release.

## Judge boundary

`imported-unverified` and `translated-unverified` explicitly mean that repository
checks are not authenticated LeetCode Accepted submissions. No blanket Accepted
claim is made. Generated coverage is a count of real files, not a proof that every
implementation passes every judge case.
