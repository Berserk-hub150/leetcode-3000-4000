from typing import List


class Solution:
    def largestSquareArea(self, bottomLeft: List[List[int]], topRight: List[List[int]]) -> int:
        best = 0
        for i in range(len(bottomLeft)):
            for j in range(i + 1, len(bottomLeft)):
                width = min(topRight[i][0], topRight[j][0]) - max(bottomLeft[i][0], bottomLeft[j][0])
                height = min(topRight[i][1], topRight[j][1]) - max(bottomLeft[i][1], bottomLeft[j][1])
                side = min(width, height)
                if side > 0:
                    best = max(best, side)
        return best * best
