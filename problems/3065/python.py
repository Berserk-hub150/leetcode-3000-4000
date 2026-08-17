from typing import List


class Solution:
    def minOperations(self, nums: List[int], k: int) -> int:
        return sum(value < k for value in nums)
