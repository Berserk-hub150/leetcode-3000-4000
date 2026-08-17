from typing import List


class Solution:
    def canSortArray(self, nums: List[int]) -> bool:
        previous_max = -1
        i = 0
        while i < len(nums):
            bits = nums[i].bit_count()
            j = i
            block_min = block_max = nums[i]
            while j < len(nums) and nums[j].bit_count() == bits:
                block_min = min(block_min, nums[j])
                block_max = max(block_max, nums[j])
                j += 1
            if block_min < previous_max:
                return False
            previous_max = block_max
            i = j
        return True
