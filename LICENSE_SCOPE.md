# License scope

This archive is multi-licensed. The root MIT license covers original repository
work; it does not replace the licenses of imported or adapted solutions.

| Material | License | Identification |
|---|---|---|
| Original scripts, metadata, documentation and original solutions | MIT | No third-party source for that file/language |
| doocs-derived implementations and their adaptations | CC BY-SA 4.0 | `upstream.repository` is `doocs/leetcode`, unless a more specific per-language record applies |
| Kamyu implementations | MIT | Language appears in `secondary_upstream.files` |
| New imported Java implementations | MIT | Language appears in `additional_sources`, identifying `leetcode_java` or `walkccc` |
| Java adaptations of existing C++ | Same license as the identified source | `adapted_sources.java` and the Java SPDX/source header; 47 MIT, 1 CC BY-SA 4.0 |

For a solution file, resolve its canonical language using `languages.json`.
Then use an explicit per-language `adapted_sources` entry first, then
`additional_sources`, followed by
`secondary_upstream.files`, followed by the doocs `upstream` record for an
`imported-unverified` language. Locally authored languages that are not marked
imported do not inherit a license merely because the directory has an upstream
record for a different language. Explicit adaptation records take precedence.

`source_patches` identifies local fixes applied to otherwise imported files.
Those fixes retain the source license; their exact transformations and regression
tests are versioned in `scripts/source_patches.py` and `scripts/test_java_translations.py`.

Complete license texts and original copyright notices are in `LICENSES/`.
Source revisions are pinned in `sources.lock.json`; problem metadata supplies
the source paths. Preserve these notices when redistributing the code.
