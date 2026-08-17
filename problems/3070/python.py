from typing import List


class Solution:
    def countSubmatrices(self, grid: List[List[int]], k: int) -> int:
        rows, cols = len(grid), len(grid[0])
        column_sums = [0] * cols
        answer = 0
        for r in range(rows):
            running = 0
            for c in range(cols):
                column_sums[c] += grid[r][c]
                running += column_sums[c]
                if running <= k:
                    answer += 1
        return answer
