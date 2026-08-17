from typing import List


class Solution:
    def earliestSecondToMarkIndices(self, nums: List[int], changeIndices: List[int]) -> int:
        n, m = len(nums), len(changeIndices)

        def feasible(seconds: int) -> bool:
            last = [-1] * n
            for time in range(seconds):
                last[changeIndices[time] - 1] = time
            if any(time < 0 for time in last):
                return False
            free = 0
            for time in range(seconds):
                index = changeIndices[time] - 1
                if last[index] == time:
                    if free < nums[index]:
                        return False
                    free -= nums[index]
                else:
                    free += 1
            return True

        lo, hi = 1, m + 1
        while lo < hi:
            mid = (lo + hi) // 2
            if feasible(mid):
                hi = mid
            else:
                lo = mid + 1
        return -1 if lo == m + 1 else lo
