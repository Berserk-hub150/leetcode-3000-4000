from typing import List


class Solution:
    def minimumOperationsToWriteY(self, grid: List[List[int]]) -> int:
        n = len(grid)
        mid = n // 2
        y_count = [0, 0, 0]
        other_count = [0, 0, 0]
        y_cells = 0

        for r in range(n):
            for c in range(n):
                on_y = (r <= mid and (c == r or c == n - 1 - r)) or (r > mid and c == mid)
                if on_y:
                    y_count[grid[r][c]] += 1
                    y_cells += 1
                else:
                    other_count[grid[r][c]] += 1

        other_cells = n * n - y_cells
        return min(
            (y_cells - y_count[y_color]) + (other_cells - other_count[other_color])
            for y_color in range(3)
            for other_color in range(3)
            if y_color != other_color
        )
