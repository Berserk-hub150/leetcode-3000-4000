from typing import List


class Solution:
    def maximumSubarraySum(self, nums: List[int], k: int) -> int:
        smallest_prefix = {}
        prefix = 0
        best = None

        for value in nums:
            old = smallest_prefix.get(value)
            if old is None or prefix < old:
                smallest_prefix[value] = prefix

            prefix += value
            for wanted in (value - k, value + k):
                if wanted in smallest_prefix:
                    candidate = prefix - smallest_prefix[wanted]
                    best = candidate if best is None else max(best, candidate)
        return 0 if best is None else best
