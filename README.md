# LeetCode 3000–4000

A structured, multi-language collection of solutions for LeetCode problems **#3000 through #4000**.

> Status: 🚧 building in private. Solutions are marked as verified only after review/testing; placeholders are never counted as solved.

## Goal

- Problems covered: **1001** (`3000` … `4000`)
- Multiple languages per problem
- Concise approach and complexity notes
- Machine-readable metadata
- Automatic progress/index generation
- CI validation before publication

## Repository layout

```text
problems/
  3000/
    metadata.json
    README.md
    python.py
    cpp.cpp
    java.java
    ...
scripts/
  bootstrap.py
  generate_index.py
  validate.py
.github/workflows/
  validate.yml
```

## Solution status

Each language entry can be:

- `verified` — reviewed/tested against the problem contract
- `unverified` — implementation exists but still needs verification
- `missing` — not implemented yet

Only `verified` solutions count toward completion.

## Languages

The repository is designed to accommodate the languages commonly supported by LeetCode, including Python, C++, Java, C, C#, JavaScript, TypeScript, Go, Rust, Kotlin, Swift, Ruby, PHP, Scala, Dart, Racket and Erlang where applicable.

## Progress

The generated progress table will live in [`INDEX.md`](INDEX.md).

## Copyright note

This repository stores original solution code, concise original explanations, problem numbers/titles, and links to the official LeetCode pages. It does **not** mirror full LeetCode problem statements.
