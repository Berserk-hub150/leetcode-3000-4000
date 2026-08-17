# LeetCode 3000–4000

A structured, multi-language solution archive for every LeetCode problem ID from **#3000 through #4000**.

> **Numeric coverage is complete:** every ID in the range has at least one solution file. Imported implementations remain explicitly marked as unverified until independently checked against the LeetCode judge.

## Current progress

- **1001 / 1001 problem IDs covered**
- **0 problem IDs missing a solution**
- **4,504 solution files currently present**
- Multiple implementations are available for many problems
- Existing local solutions are never overwritten by the import/enrichment workflows

See [`COVERAGE.md`](COVERAGE.md) for the exact live counts and [`NOTICE.md`](NOTICE.md) for third-party attribution.

### Current files by language / extension

| Language | Files |
|---|---:|
| Python | 976 |
| C++ | 932 |
| Java | 750 |
| Go | 741 |
| TypeScript | 701 |
| Rust | 179 |
| SQL | 74 |
| C# | 62 |
| JavaScript | 30 |
| PHP | 9 |
| C | 8 |
| Swift | 6 |
| Scala | 6 |
| Dart | 5 |
| Elixir | 5 |
| Ruby | 5 |
| Racket | 5 |
| Erlang | 5 |
| Kotlin | 5 |

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
  import_doocs.py
  import_kamyu.py
  enrich_kamyu_languages.py
  report_coverage.py

.github/workflows/
  validate.yml
  import-solutions.yml
  import-kamyu.yml
  enrich-languages.yml
  report-coverage.yml
```

## Status model

Language implementations can be marked as:

- `verified` — independently reviewed/tested against the problem contract
- `unverified` — implementation exists but still needs independent verification
- `imported-unverified` — implementation was imported from an attributed upstream open-source collection and has not been independently re-verified here
- `missing` — no implementation for that language

**Coverage and verification are intentionally separate metrics.** A problem counts as covered when at least one implementation exists; it is not automatically claimed to be judge-verified.

## Languages

The repository can accommodate the main LeetCode language families, including Python, C++, Java, C, C#, JavaScript, TypeScript, Go, Rust, Kotlin, Swift, Ruby, PHP, Scala, Dart, Racket, Erlang and Elixir, plus SQL/Pandas solutions where the problem type requires them.

Not every problem is available in every language. The archive preserves every available attributed implementation it can obtain without overwriting an existing solution.

## Automation

- `scripts/import_doocs.py` imports missing solution snippets from `doocs/leetcode` while preserving attribution and existing files.
- `scripts/import_kamyu.py` fills problem IDs that otherwise have no solution using the MIT-licensed `kamyu104/LeetCode-Solutions` collection.
- `scripts/enrich_kamyu_languages.py` adds additional language variants without overwriting existing implementations.
- `scripts/report_coverage.py` calculates exact range and language-file coverage.
- `scripts/validate.py` validates repository metadata and solution status values.
- GitHub Actions run the import, enrichment, coverage and validation workflows.

## Attribution and copyright

This repository does **not** mirror full LeetCode problem statements. It stores solution code, minimal problem metadata and links to the official LeetCode pages.

Some implementations are independently authored in this repository. Others are imported from open-source solution collections under their respective licenses. See [`NOTICE.md`](NOTICE.md) and each problem's `metadata.json` for source attribution and license information.
