# LeetCode 3000–4000

A structured, multi-language solution archive for every LeetCode problem ID from **#3000 through #4000**.

> **Complete numeric coverage:** every ID in the range has at least one solution file. The repository also runs source-integrity, language-aware syntax and multi-runtime behavioral verification. Individual authenticated LeetCode `Accepted` submissions are treated separately from repository verification.

## Current progress

- **1001 / 1001 problem IDs covered**
- **0 problem IDs missing a solution**
- **4,477 canonical solution files currently present**
- **4,477 / 4,477 current solution files covered by repository verification**
  - **4,419** imported/source-backed files match their recorded upstream implementation
  - **58** residual translated variants compile/run and pass deterministic behavioral tests in their real language runtimes
- **4,477 / 4,477** files pass language-aware syntax parsing
- **1001 / 1001** problem slugs have a known reference solution source

See [`COVERAGE.md`](COVERAGE.md) for exact live counts, [`VERIFICATION.md`](VERIFICATION.md) for the verification evidence, [`EXTRA_VARIANT_VERIFICATION.md`](EXTRA_VARIANT_VERIFICATION.md) for the 58 multi-runtime tests, and [`NOTICE.md`](NOTICE.md) for third-party attribution.

### Current files by language / extension

| Language | Files |
|---|---:|
| Python | 976 |
| C++ | 927 |
| Java | 745 |
| Go | 736 |
| TypeScript | 696 |
| Rust | 175 |
| SQL | 74 |
| C# | 60 |
| JavaScript | 29 |
| PHP | 9 |
| C | 8 |
| Scala | 6 |
| Swift | 6 |
| Ruby | 5 |
| Dart | 5 |
| Kotlin | 5 |
| Erlang | 5 |
| Elixir | 5 |
| Racket | 5 |

## Repository layout

```text
problems/
  3000/
    metadata.json
    python.py
    cpp.cpp
    java.java
    ...
  3001/
  ...
  4000/

scripts/
  bootstrap.py
  generate_index.py
  validate.py
  syntax_check.py
  verify_reference_coverage.py
  verify_import_integrity.py
  verify_extra_variants.py
  import_doocs.py
  import_kamyu.py
  enrich_kamyu_languages.py
  source_back_local_solutions.py
  normalize_solution_filenames.py
  report_coverage.py

.github/workflows/
  validate.yml
  verify-extra-variants.yml
  import-solutions.yml
  import-kamyu.yml
  enrich-languages.yml
  source-back.yml
  normalize-filenames.yml
  report-coverage.yml
```

## Verification model

Repository verification has two complementary paths:

1. **Source-backed implementations** — imported code must reproduce the attributed upstream solution for the same problem/language. CI currently checks **4,419** such files.
2. **Extra language variants** — variants without a configured same-language upstream reference are compiled and executed against behavioral test cases in the real runtime. The current residual set is **58 / 58 passing**.

All current files are additionally parsed using their language grammar or SQL dialect. Python files are bytecode-compiled, and selected languages receive additional native syntax checks.

Metadata values such as `imported-unverified` intentionally do **not** mean “unchecked file.” They distinguish repository verification from an authenticated LeetCode judge submission. A literal LeetCode `Accepted` claim is only appropriate after that exact file has actually been submitted to the judge.

## Languages

The repository accommodates Python, C++, Java, C, C#, JavaScript, TypeScript, Go, Rust, Kotlin, Swift, Ruby, PHP, Scala, Dart, Racket, Erlang and Elixir, plus SQL/Pandas solutions where the problem type requires them.

Not every problem has a solution in every language. The archive keeps every canonical implementation available for that problem without counting same-language legacy duplicates twice.

## Automation

- `scripts/validate.py` requires complete **3000–4000** coverage and non-empty solution files.
- `scripts/syntax_check.py` parses every solution using the appropriate language grammar / SQL dialect.
- `scripts/verify_reference_coverage.py` verifies all **1001** problem slugs against known solution sources.
- `scripts/verify_import_integrity.py` reconstructs and compares imported/source-backed implementations.
- `scripts/verify_extra_variants.py` compiles/executes the 58 residual language variants against behavioral tests.
- `scripts/normalize_solution_filenames.py` removes same-language legacy duplicates while preserving canonical variants.
- `scripts/report_coverage.py` regenerates exact live coverage counts.
- GitHub Actions enforce the checks continuously.

## Attribution and copyright

This repository does **not** mirror full LeetCode problem statements. It stores solution code, minimal problem metadata and links to the official LeetCode pages.

Some implementations are independently authored in this repository. Others are imported from open-source solution collections under their respective licenses. See [`NOTICE.md`](NOTICE.md) and each problem's `metadata.json` for source attribution and license information.
