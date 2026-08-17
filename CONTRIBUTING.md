# Contributing

Contributions should add or improve an **original solution** for a problem in the range **3000–4000**.

## Rules

1. Do not paste full LeetCode problem statements.
2. Keep the problem number, title, official link, original explanation and complexity notes.
3. Mark a language `verified` only when the implementation has been checked against the current LeetCode signature/contract.
4. Do not submit generated placeholders as solved problems.
5. Prefer one focused problem or language improvement per pull request.

## Language files

Canonical filenames are defined in `languages.json`.

## Metadata

Each problem has a `metadata.json` file. Example:

```json
{
  "number": 3000,
  "title": "Maximum Area of Longest Diagonal Rectangle",
  "slug": "maximum-area-of-longest-diagonal-rectangle",
  "url": "https://leetcode.com/problems/maximum-area-of-longest-diagonal-rectangle/",
  "difficulty": "Easy",
  "status": "verified",
  "languages": {
    "python3": "verified",
    "cpp": "verified"
  }
}
```
