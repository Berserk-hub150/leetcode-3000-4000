from collections import Counter
from typing import List


class Solution:
    def maximumLength(self, nums: List[int]) -> int:
        freq = Counter(nums)
        ones = freq.pop(1, 0)
        answer = ones if ones % 2 else max(0, ones - 1)

        for start in list(freq):
            length = 0
            value = start
            while freq.get(value, 0) >= 2:
                length += 2
                value *= value
            if freq.get(value, 0) >= 1:
                length += 1
            else:
                length -= 1
            answer = max(answer, length)
        return max(answer, 1)
