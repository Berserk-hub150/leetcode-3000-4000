from bisect import bisect_left
from typing import List


class Solution:
    def beautifulIndices(self, s: str, a: str, b: str, k: int) -> List[int]:
        def occurrences(pattern: str) -> List[int]:
            m = len(pattern)
            pi = [0] * m
            for i in range(1, m):
                j = pi[i - 1]
                while j and pattern[i] != pattern[j]:
                    j = pi[j - 1]
                if pattern[i] == pattern[j]:
                    j += 1
                pi[i] = j

            found = []
            j = 0
            for i, ch in enumerate(s):
                while j and ch != pattern[j]:
                    j = pi[j - 1]
                if ch == pattern[j]:
                    j += 1
                if j == m:
                    found.append(i - m + 1)
                    j = pi[j - 1]
            return found

        aa = occurrences(a)
        bb = occurrences(b)
        answer = []
        for i in aa:
            j = bisect_left(bb, i - k)
            if j < len(bb) and bb[j] <= i + k:
                answer.append(i)
        return answer
