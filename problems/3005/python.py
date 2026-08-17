from collections import Counter
from typing import List


class Solution:
    def maxFrequencyElements(self, nums: List[int]) -> int:
        freq = Counter(nums)
        best = max(freq.values())
        return sum(v for v in freq.values() if v == best)
