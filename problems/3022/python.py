from typing import List


class Solution:
    def minOrAfterOperations(self, nums: List[int], k: int) -> int:
        answer = 0
        forced_zero_mask = 0
        required_segments = len(nums) - k

        for bit in range(29, -1, -1):
            trial = forced_zero_mask | (1 << bit)
            segments = 0
            running = (1 << 30) - 1
            for value in nums:
                running &= value
                if running & trial == 0:
                    segments += 1
                    running = (1 << 30) - 1
            if segments >= required_segments:
                forced_zero_mask = trial
            else:
                answer |= 1 << bit
        return answer
