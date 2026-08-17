from collections import defaultdict
from typing import List


class Solution:
    def maxIntersectionCount(self, y: List[int]) -> int:
        events = defaultdict(int)
        n = len(y)
        for i in range(1, n):
            start = 2 * y[i - 1]
            finish = 2 * y[i]
            if i != n - 1:
                finish += -1 if y[i] > y[i - 1] else 1
            lo, hi = sorted((start, finish))
            events[lo] += 1
            events[hi + 1] -= 1

        active = answer = 0
        for coordinate in sorted(events):
            active += events[coordinate]
            answer = max(answer, active)
        return answer
