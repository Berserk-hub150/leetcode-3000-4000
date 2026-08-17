from typing import List


class Solution:
    def maximumStrength(self, nums: List[int], k: int) -> int:
        neg = -10**30
        outside = [neg] * (k + 1)
        inside = [neg] * (k + 1)
        outside[0] = 0

        for value in nums:
            new_outside = outside[:]
            new_inside = [neg] * (k + 1)
            for chosen in range(1, k + 1):
                coefficient = (k - chosen + 1) * (1 if chosen % 2 else -1)
                contribution = coefficient * value
                new_inside[chosen] = max(
                    inside[chosen] + contribution,
                    outside[chosen - 1] + contribution,
                    inside[chosen - 1] + contribution,
                )
                new_outside[chosen] = max(outside[chosen], inside[chosen])
            outside, inside = new_outside, new_inside
        return max(outside[k], inside[k])
