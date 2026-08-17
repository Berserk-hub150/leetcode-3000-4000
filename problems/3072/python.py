from bisect import bisect_left
from typing import List


class Fenwick:
    def __init__(self, size: int):
        self.tree = [0] * (size + 1)

    def add(self, index: int) -> None:
        while index < len(self.tree):
            self.tree[index] += 1
            index += index & -index

    def query(self, index: int) -> int:
        total = 0
        while index:
            total += self.tree[index]
            index -= index & -index
        return total


class Solution:
    def resultArray(self, nums: List[int]) -> List[int]:
        values = sorted(set(nums))
        first, second = [nums[0]], [nums[1]]
        bit1, bit2 = Fenwick(len(values)), Fenwick(len(values))
        bit1.add(bisect_left(values, nums[0]) + 1)
        bit2.add(bisect_left(values, nums[1]) + 1)

        for value in nums[2:]:
            rank = bisect_left(values, value) + 1
            greater1 = len(first) - bit1.query(rank)
            greater2 = len(second) - bit2.query(rank)
            if greater1 > greater2 or (greater1 == greater2 and len(first) <= len(second)):
                first.append(value)
                bit1.add(rank)
            else:
                second.append(value)
                bit2.add(rank)
        return first + second
