from typing import List


class Solution:
    def minimumArrayLength(self, nums: List[int]) -> int:
        smallest = min(nums)
        smallest_count = 0
        for value in nums:
            if value % smallest:
                return 1
            if value == smallest:
                smallest_count += 1
        return (smallest_count + 1) // 2
