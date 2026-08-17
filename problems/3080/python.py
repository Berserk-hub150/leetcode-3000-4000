import heapq
from typing import List


class Solution:
    def unmarkedSumArray(self, nums: List[int], queries: List[List[int]]) -> List[int]:
        heap = [(value, i) for i, value in enumerate(nums)]
        heapq.heapify(heap)
        marked = [False] * len(nums)
        remaining = sum(nums)
        answer = []

        for index, count in queries:
            if not marked[index]:
                marked[index] = True
                remaining -= nums[index]
            while count:
                while heap and marked[heap[0][1]]:
                    heapq.heappop(heap)
                if not heap:
                    break
                value, i = heapq.heappop(heap)
                marked[i] = True
                remaining -= value
                count -= 1
            answer.append(remaining)
        return answer
