from typing import List


class Solution:
    def maxOperations(self, nums: List[int]) -> int:
        target = nums[0] + nums[1]
        operations = 0
        for i in range(0, len(nums) - 1, 2):
            if nums[i] + nums[i + 1] != target:
                break
            operations += 1
        return operations
