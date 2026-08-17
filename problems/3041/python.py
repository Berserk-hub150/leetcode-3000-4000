from typing import List


class Solution:
    def maxSelectedElements(self, nums: List[int]) -> int:
        nums.sort()
        dp = {}
        answer = 0
        for x in nums:
            end_at_x = dp.get(x - 1, 0) + 1
            end_at_x_plus_one = dp.get(x, 0) + 1
            dp[x + 1] = max(dp.get(x + 1, 0), end_at_x_plus_one)
            dp[x] = max(dp.get(x, 0), end_at_x)
            answer = max(answer, dp[x], dp[x + 1])
        return answer
