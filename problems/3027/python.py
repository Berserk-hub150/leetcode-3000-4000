from typing import List


class Solution:
    def numberOfPairs(self, points: List[List[int]]) -> int:
        ordered = sorted(points, key=lambda p: (p[0], -p[1]))
        result = 0
        for i, (_, top) in enumerate(ordered):
            lower_bound = float("-inf")
            for _, y in ordered[i + 1:]:
                if lower_bound < y <= top:
                    result += 1
                    lower_bound = y
        return result
