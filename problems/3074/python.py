from typing import List


class Solution:
    def minimumBoxes(self, apple: List[int], capacity: List[int]) -> int:
        remaining = sum(apple)
        for boxes, size in enumerate(sorted(capacity, reverse=True), 1):
            remaining -= size
            if remaining <= 0:
                return boxes
        return len(capacity)
