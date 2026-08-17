from bisect import bisect_left
from typing import List


class Solution:
    def beautifulIndices(self, s: str, a: str, b: str, k: int) -> List[int]:
        def matches(pattern: str) -> List[int]:
            m = len(pattern)
            return [i for i in range(len(s) - m + 1) if s.startswith(pattern, i)]

        left = matches(a)
        right = matches(b)
        answer = []
        for i in left:
            p = bisect_left(right, i - k)
            if p < len(right) and right[p] <= i + k:
                answer.append(i)
        return answer
