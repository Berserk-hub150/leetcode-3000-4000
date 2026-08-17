# Third-party attribution

This repository contains two kinds of solution files:

1. Solutions authored directly for this repository.
2. Missing language implementations imported by `scripts/import_doocs.py` from the open-source [`doocs/leetcode`](https://github.com/doocs/leetcode) project.

The importer deliberately extracts **solution code only** plus minimal metadata. It does not mirror full LeetCode problem statements.

## doocs/leetcode

Imported files whose adjacent `metadata.json` contains an `upstream` field are derived from **doocs/leetcode** and remain subject to that project's **Creative Commons Attribution-ShareAlike 4.0 International (CC BY-SA 4.0)** license.

- Upstream project: https://github.com/doocs/leetcode
- Upstream license: https://github.com/doocs/leetcode/blob/main/LICENSE
- Changes made here: snippets are extracted from the upstream Markdown layout, renamed into per-language files, combined with local metadata, and may coexist with independently authored local implementations.

No affiliation with or endorsement by LeetCode or the upstream maintainers is implied.
