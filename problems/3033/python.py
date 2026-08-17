from typing import List


class Solution:
    def modifiedMatrix(self, matrix: List[List[int]]) -> List[List[int]]:
        rows, cols = len(matrix), len(matrix[0])
        column_max = [max(matrix[r][c] for r in range(rows)) for c in range(cols)]
        return [
            [column_max[c] if matrix[r][c] == -1 else matrix[r][c] for c in range(cols)]
            for r in range(rows)
        ]
