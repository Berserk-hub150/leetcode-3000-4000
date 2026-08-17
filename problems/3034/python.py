from typing import List


class Solution:
    def countMatchingSubarrays(self, nums: List[int], pattern: List[int]) -> int:
        m = len(pattern)
        answer = 0
        for start in range(len(nums) - m):
            ok = True
            for j, expected in enumerate(pattern):
                a, b = nums[start + j], nums[start + j + 1]
                relation = 1 if b > a else -1 if b < a else 0
                if relation != expected:
                    ok = False
                    break
            answer += ok
        return answer
