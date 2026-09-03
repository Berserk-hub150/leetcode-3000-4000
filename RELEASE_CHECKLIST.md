# Release checklist

- [x] Full license texts, explicit per-language license scope and adaptation notices.
- [x] Complete generated index: 1,001 problems, 4,659 canonical files.
- [x] C++ and Java for all 927 algorithm problems; 74 SQL tasks separately documented.
- [x] Immutable upstream revisions and source-integrity checks.
- [x] Canonical filenames and metadata/file consistency enforced.
- [x] Read-only automatic validation; repository-writing workflows manual only.
- [x] Obsolete BATCH_3000_3040.md and BATCH_3041_3081.md removed (recoverable from Git history).
- [x] 182 Java additions compiled; 48 adaptations pass 2,304 differential cases
  and 1,008 independent-oracle checks. All 927 Java files compile with the
  judge-like JDK 17 harness after compatibility fixes.
- [ ] Confirm successful Actions runs for the exact release commit.
- [ ] Set the GitHub repository description and topics in the About panel.
- [ ] Change visibility only when the owner is ready. This maintenance does not publish the repository.

Suggested description:

> LeetCode 3000–4000: 1001 problems, 4659 implementations, complete C++/Java coverage for algorithm tasks, pinned sources and explicit licenses.

Suggested topics:

`leetcode`, `algorithms`, `data-structures`, `cpp`, `java`, `python`, `sql`,
`coding-interview`, `competitive-programming`, `leetcode-solutions`.

The connected GitHub integration used for this maintenance supports repository
content updates but does not expose description/topic updates. Those settings
are intentionally left unchecked rather than reported as completed.
