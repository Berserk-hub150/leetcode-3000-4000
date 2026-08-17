from functools import lru_cache


class Solution:
    def maxPartitionsAfterOperations(self, s: str, k: int) -> int:
        n = len(s)

        @lru_cache(maxsize=None)
        def solve(i: int, mask: int, changed: bool) -> int:
            if i == n:
                return 1

            bit = 1 << (ord(s[i]) - 97)
            merged = mask | bit
            if merged.bit_count() > k:
                best = 1 + solve(i + 1, bit, changed)
            else:
                best = solve(i + 1, merged, changed)

            if not changed:
                for c in range(26):
                    replacement = 1 << c
                    merged = mask | replacement
                    if merged.bit_count() > k:
                        candidate = 1 + solve(i + 1, replacement, True)
                    else:
                        candidate = solve(i + 1, merged, True)
                    best = max(best, candidate)
            return best

        return solve(0, 0, False)
