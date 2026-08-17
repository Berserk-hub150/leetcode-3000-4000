from functools import lru_cache
from typing import List


class Solution:
    def maxOperations(self, nums: List[int]) -> int:
        n = len(nums)
        if n < 2:
            return 0

        def run(left: int, right: int, target: int) -> int:
            @lru_cache(maxsize=None)
            def dp(l: int, r: int) -> int:
                if r - l + 1 < 2:
                    return 0
                best = 0
                if nums[l] + nums[l + 1] == target:
                    best = max(best, 1 + dp(l + 2, r))
                if nums[r - 1] + nums[r] == target:
                    best = max(best, 1 + dp(l, r - 2))
                if nums[l] + nums[r] == target:
                    best = max(best, 1 + dp(l + 1, r - 1))
                return best
            return dp(left, right)

        answer = 1 + run(2, n - 1, nums[0] + nums[1])
        answer = max(answer, 1 + run(0, n - 3, nums[-2] + nums[-1]))
        answer = max(answer, 1 + run(1, n - 2, nums[0] + nums[-1]))
        return answer
