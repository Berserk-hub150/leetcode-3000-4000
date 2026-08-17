from typing import List


class Solution:
    def resultArray(self, nums: List[int]) -> List[int]:
        first = [nums[0]]
        second = [nums[1]]
        for value in nums[2:]:
            if first[-1] > second[-1]:
                first.append(value)
            else:
                second.append(value)
        return first + second
