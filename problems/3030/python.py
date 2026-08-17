from typing import List


class Solution:
    def resultGrid(self, image: List[List[int]], threshold: int) -> List[List[int]]:
        rows, cols = len(image), len(image[0])
        total = [[0] * cols for _ in range(rows)]
        count = [[0] * cols for _ in range(rows)]

        for r in range(rows - 2):
            for c in range(cols - 2):
                valid = True
                for i in range(r, r + 3):
                    for j in range(c, c + 2):
                        if abs(image[i][j] - image[i][j + 1]) > threshold:
                            valid = False
                for i in range(r, r + 2):
                    for j in range(c, c + 3):
                        if abs(image[i][j] - image[i + 1][j]) > threshold:
                            valid = False
                if not valid:
                    continue
                average = sum(image[i][j] for i in range(r, r + 3) for j in range(c, c + 3)) // 9
                for i in range(r, r + 3):
                    for j in range(c, c + 3):
                        total[i][j] += average
                        count[i][j] += 1

        return [
            [total[r][c] // count[r][c] if count[r][c] else image[r][c] for c in range(cols)]
            for r in range(rows)
        ]
