from collections import Counter
from math import isqrt
from typing import List


class Solution:
    def mostFrequentPrime(self, mat: List[List[int]]) -> int:
        rows, cols = len(mat), len(mat[0])
        directions = [(dr, dc) for dr in (-1, 0, 1) for dc in (-1, 0, 1) if dr or dc]
        counts = Counter()

        def prime(value: int) -> bool:
            if value < 2:
                return False
            if value % 2 == 0:
                return value == 2
            d = 3
            while d <= isqrt(value):
                if value % d == 0:
                    return False
                d += 2
            return True

        for r in range(rows):
            for c in range(cols):
                for dr, dc in directions:
                    nr, nc = r + dr, c + dc
                    value = mat[r][c]
                    while 0 <= nr < rows and 0 <= nc < cols:
                        value = value * 10 + mat[nr][nc]
                        if value > 10 and prime(value):
                            counts[value] += 1
                        nr += dr
                        nc += dc
        if not counts:
            return -1
        best_frequency = max(counts.values())
        return max(value for value, frequency in counts.items() if frequency == best_frequency)
