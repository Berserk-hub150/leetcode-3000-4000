from typing import List


class Fenwick:
    def __init__(self, n: int):
        self.n = n
        self.count = [0] * (n + 1)
        self.total = [0] * (n + 1)

    def add(self, i: int, dc: int, ds: int) -> None:
        while i <= self.n:
            self.count[i] += dc
            self.total[i] += ds
            i += i & -i

    def prefix(self, tree, i: int) -> int:
        out = 0
        while i:
            out += tree[i]
            i -= i & -i
        return out

    def sum_smallest(self, need: int, values: List[int]) -> int:
        if need == 0:
            return 0
        idx = 0
        seen = 0
        step = 1 << (self.n.bit_length() - 1)
        while step:
            nxt = idx + step
            if nxt <= self.n and seen + self.count[nxt] < need:
                idx = nxt
                seen += self.count[nxt]
            step >>= 1
        before_sum = self.prefix(self.total, idx)
        take = need - seen
        return before_sum + take * values[idx]


class Solution:
    def minimumCost(self, nums: List[int], k: int, dist: int) -> int:
        need = k - 1
        values = sorted(set(nums[1:]))
        rank = {v: i + 1 for i, v in enumerate(values)}
        bit = Fenwick(len(values))

        def insert(v: int, delta: int) -> None:
            bit.add(rank[v], delta, delta * v)

        right = min(len(nums) - 1, dist + 1)
        for i in range(1, right + 1):
            insert(nums[i], 1)
        answer = bit.sum_smallest(need, values)

        for left in range(2, len(nums) - dist):
            insert(nums[left - 1], -1)
            new_right = left + dist
            if new_right < len(nums):
                insert(nums[new_right], 1)
            answer = min(answer, bit.sum_smallest(need, values))
        return nums[0] + answer
