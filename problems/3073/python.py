from bisect import bisect_left
from typing import List


class FenwickMax:
    def __init__(self, n: int):
        self.tree = [-1] * (n + 1)

    def update(self, i: int, value: int) -> None:
        while i < len(self.tree):
            self.tree[i] = max(self.tree[i], value)
            i += i & -i

    def query(self, i: int) -> int:
        answer = -1
        while i:
            answer = max(answer, self.tree[i])
            i -= i & -i
        return answer


class Solution:
    def maximumTripletValue(self, nums: List[int]) -> int:
        n = len(nums)
        suffix = [0] * n
        suffix[-1] = nums[-1]
        for i in range(n - 2, -1, -1):
            suffix[i] = max(nums[i], suffix[i + 1])

        values = sorted(set(nums))
        bit = FenwickMax(len(values))
        bit.update(bisect_left(values, nums[0]) + 1, nums[0])
        answer = 0
        for j in range(1, n - 1):
            rank = bisect_left(values, nums[j]) + 1
            left = bit.query(rank - 1)
            right = suffix[j + 1]
            if left >= 0 and right > nums[j]:
                answer = max(answer, left - nums[j] + right)
            bit.update(rank, nums[j])
        return answer
