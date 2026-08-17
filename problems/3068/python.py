from typing import List


class Solution:
    def maximumValueSum(self, nums: List[int], k: int, edges: List[List[int]]) -> int:
        even = 0
        odd = float('-inf')
        for value in nums:
            toggled = value ^ k
            new_even = max(even + value, odd + toggled)
            new_odd = max(odd + value, even + toggled)
            even, odd = new_even, new_odd
        return even
