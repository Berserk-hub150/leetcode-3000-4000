from typing import List


class Solution:
    def areaOfMaxDiagonal(self, dimensions: List[List[int]]) -> int:
        best_diag = 0
        best_area = 0
        for length, width in dimensions:
            diag = length * length + width * width
            area = length * width
            if diag > best_diag or (diag == best_diag and area > best_area):
                best_diag = diag
                best_area = area
        return best_area
