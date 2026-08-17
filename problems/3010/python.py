from typing import List


class Solution:
    def minimumCost(self, nums: List[int]) -> int:
        first = second = float('inf')
        for x in nums[1:]:
            if x < first:
                first, second = x, first
            elif x < second:
                second = x
        return nums[0] + first + second
