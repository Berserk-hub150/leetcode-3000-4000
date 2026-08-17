from typing import List


class Solution:
    def numberOfPairs(self, points: List[List[int]]) -> int:
        points.sort(key=lambda p: (p[0], -p[1]))
        answer = 0
        for i in range(len(points)):
            upper_y = points[i][1]
            best_lower = float("-inf")
            for j in range(i + 1, len(points)):
                y = points[j][1]
                if best_lower < y <= upper_y:
                    answer += 1
                    best_lower = y
        return answer
