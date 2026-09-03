"""Small, reviewed transformations applied after extracting an immutable source.

These are not arbitrary replacement instructions from metadata. Each patch is
restricted to one problem/language and requires exactly one matching context.
"""
PATCHES = {
    '3625-java17-1': (3625, "java", '                cnt1.computeIfAbsent(k, _ -> new HashMap<>()).merge(b, 1, Integer::sum);\n', '                cnt1.computeIfAbsent(k, unused -> new HashMap<>()).merge(b, 1, Integer::sum);\n'),
    '3625-java17-2': (3625, "java", '                cnt2.computeIfAbsent(p, _ -> new HashMap<>()).merge(k, 1, Integer::sum);\n', '                cnt2.computeIfAbsent(p, unused -> new HashMap<>()).merge(k, 1, Integer::sum);\n'),
    '3709-java17-1': (3709, "java", '        pre.add(pre.getLast() + score);\n', '        pre.add(pre.get(pre.size() - 1) + score);\n'),
    '3748-java17-1': (3748, "java", '                s.add(s.getLast() + (long) k * (k + 1) / 2);\n', '                s.add(s.get(s.size() - 1) + (long) k * (k + 1) / 2);\n'),
    '3822-java17-1': (3822, "java", '        t.computeIfAbsent(key, _ -> new ArrayList<>()).add(orderId);\n', '        t.computeIfAbsent(key, unused -> new ArrayList<>()).add(orderId);\n'),
    '3822-java17-2': (3822, "java", '        t.computeIfAbsent(new Key(orderType, newPrice), _ -> new ArrayList<>()).add(orderId);\n', '        t.computeIfAbsent(new Key(orderType, newPrice), unused -> new ArrayList<>()).add(orderId);\n'),
    "3933-owned-bounds": (3933, "cpp",
        "                const auto& r1 = max(r - x, 0);\n"
        "                const auto& r2 = min(r + x, n - 1);\n"
        "                const auto& c1 = max(c - x, 0);\n"
        "                const auto& c2 = min(c + x, m - 1);\n",
        "                const int r1 = max(r - x, 0);\n"
        "                const int r2 = min(r + x, n - 1);\n"
        "                const int c1 = max(c - x, 0);\n"
        "                const int c2 = min(c + x, m - 1);\n"),
    "3933-empty-range": (3933, "cpp",
        "        int query(int r1, int c1, int r2, int c2) const {\n",
        "        int query(int r1, int c1, int r2, int c2) const {\n"
        "            // Local fix: excluding corners can leave an empty rectangle.\n"
        "            if (r1 > r2 || c1 > c2) return numeric_limits<int>::min();\n"),
    "3953-own-maximum": (3953, "cpp",
        "        const auto& mx = max(ranges::max(nums), maxVal);\n",
        "        const auto mx = max(ranges::max(nums), maxVal);  // Local fix: own the value, not a dangling reference.\n"),
}


def apply_source_patches(text: str, number: int, language: str, names: list[str]) -> str:
    for name in names:
        expected_number, expected_language, before, after = PATCHES[name]
        if (number, language) != (expected_number, expected_language):
            raise ValueError(f"Patch {name} is not valid for {number}/{language}")
        if text.count(before) != 1:
            raise ValueError(f"Patch {name} does not match its immutable source exactly once")
        text = text.replace(before, after, 1)
    return text
