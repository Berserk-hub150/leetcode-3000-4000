# LeetCode 3000–4000

A multi-language archive covering all **1,001 problem IDs**, with **4,659 canonical
solution files**. Every one of the **927 algorithm problems has both C++ and Java**.
The other **74 problems are SQL/database tasks**, which do not support native
C++/Java submissions on LeetCode; they retain their SQL/Pandas implementations.

[Browse all solutions](INDEX.md) · [Exact coverage](COVERAGE.md) ·
[Verification evidence](VERIFICATION.md) · [Contributing](CONTRIBUTING.md)

## What is included

Each `problems/<number>/` directory contains minimal problem metadata, an official
LeetCode link and real implementations. [languages.json](languages.json) defines
the canonical filenames: `cpp.cpp`, `java.java`, `python.py`, `csharp.cs`, and so on.
Full LeetCode problem statements are not mirrored.

The pre-release additions comprise 134 attributed Java imports and 48 Java
adaptations. The existing C++ collection already covered all 927 algorithm tasks;
two C++ files also received documented correctness/undefined-behavior fixes.

## Verification, without inflated claims

Source identity, grammar parsing, compilation, behavioral tests and LeetCode
judge acceptance are distinct checks. **This archive does not claim that every
file has an authenticated Accepted submission.** See [VERIFICATION.md](VERIFICATION.md)
for the scope and limitations of each check.

Automatic validation is read-only and checks complete coverage, canonical names,
generated-document freshness, source integrity and regression tests. Every source
repository is pinned to a full commit SHA in [sources.lock.json](sources.lock.json).
Workflows that modify the archive can run only by manual dispatch on `main`.

Quick structural checks:

```sh
python scripts/validate.py
python scripts/generate_index.py --check
python scripts/report_coverage.py --check
python -m unittest discover -s tests
```

Java additions can be checked with `python scripts/compile_java.py --new-only`.
Run `python scripts/test_java_translations.py` with JDK 17+ and a C++20 compiler
to reproduce deterministic differential tests for all 48 adaptations.

## Multiple licenses — not MIT for everything

Original repository material uses [MIT](LICENSE). Third-party files retain their
own licenses: **doocs-derived code is CC BY-SA 4.0**, while Kamyu, LeetCode-in-Java
and walkccc imports use their respective MIT notices. Java adaptations retain
the license of their identified source, including CC BY-SA for problem 3930.

Read [LICENSE_SCOPE.md](LICENSE_SCOPE.md), [NOTICE.md](NOTICE.md), the complete
texts in [LICENSES](LICENSES/), and adjacent per-language metadata before reuse.
No affiliation with LeetCode or the upstream authors is implied.
