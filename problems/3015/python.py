from typing import List


class Solution:
    def countOfPairs(self, n: int, x: int, y: int) -> List[int]:
        answer = [0] * n
        for a in range(1, n + 1):
            for b in range(a + 1, n + 1):
                direct = b - a
                via_xy = abs(a - x) + 1 + abs(b - y)
                via_yx = abs(a - y) + 1 + abs(b - x)
                distance = min(direct, via_xy, via_yx)
                answer[distance - 1] += 2
        return answer
