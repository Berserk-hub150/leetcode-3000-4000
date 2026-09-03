# Third-party attribution

This repository contains original work and attributed solution code. Full
LeetCode problem statements are not mirrored. See [LICENSE_SCOPE.md](LICENSE_SCOPE.md)
for per-file license resolution and [sources.lock.json](sources.lock.json) for
immutable source revisions.

## doocs/leetcode — CC BY-SA 4.0

- Source: https://github.com/doocs/leetcode
- License: https://creativecommons.org/licenses/by-sa/4.0/
- Full license and disclaimer: [LICENSES/CC-BY-SA-4.0.txt](LICENSES/CC-BY-SA-4.0.txt)

The adjacent metadata records the source directory. Changes consist of extracting
solution snippets from Markdown, renaming them, normalizing surrounding whitespace,
and storing minimal problem metadata. Adaptations, when present, retain CC BY-SA 4.0
and record the changes. Imported doocs code is not relicensed under MIT.

## kamyu104/LeetCode-Solutions — MIT

- Source: https://github.com/kamyu104/LeetCode-Solutions
- Copyright (c) 2018 https://github.com/kamyu104/LeetCode-Solutions
- Complete copyright, permission and warranty notice:
  [LICENSES/MIT-kamyu.txt](LICENSES/MIT-kamyu.txt)

Per-language paths are in the metadata's secondary_upstream.files mapping.
Files are copied or surrounding whitespace is normalized; filenames are changed.
This mapping takes precedence over a directory-wide doocs attribution.

47 new Java adaptations retain the Kamyu MIT attribution and record the original
C++ path, immutable revision, changes and base-file hash in `adapted_sources.java`.
The Java adaptation for problem 3930 derives from doocs and retains CC BY-SA 4.0.
Adaptations use Java-native collections/numeric types and, where appropriate,
iterative tree traversal. They are not represented as byte-identical imports.

Two imported C++ files have documented local fixes: 3933 handles empty sparse-table
query rectangles and owns its bounds, and 3953 owns its maximum value. Both avoid
dangling references. `source_patches.cpp` identifies the reproducible transformations.

Four doocs Java files (3625, 3709, 3748 and 3822) have semantics-preserving JDK 17
compatibility patches: named unused lambda parameters and indexed last-element
access instead of newer List APIs. They retain CC BY-SA 4.0 and record the exact
transformations in `source_patches.java`.

## LeetCode-in-Java/LeetCode-in-Java — MIT

- Source: https://github.com/LeetCode-in-Java/LeetCode-in-Java
- Complete copyright, permission and warranty notice:
  [LICENSES/MIT-leetcode-in-java.txt](LICENSES/MIT-leetcode-in-java.txt)

Selected Java solutions have their package declaration and top-level public
modifier removed to fit a single LeetCode file. Exact source paths and the
transformation are recorded in additional_sources.java.

## walkccc/LeetCode — MIT

- Source: https://github.com/walkccc/LeetCode
- Copyright (c) 2022 Peng-Yu Chen
- Complete copyright, permission and warranty notice:
  [LICENSES/MIT-walkccc.txt](LICENSES/MIT-walkccc.txt)

Selected Java files have standard Java imports added. Their exact source paths
and transformation are recorded in additional_sources.java.

No affiliation with or endorsement by LeetCode or any upstream author is implied.
