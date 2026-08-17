from typing import List


class Solution:
    def returnToBoundaryCount(self, nums: List[int]) -> int:
        position = 0
        answer = 0
        for move in nums:
            position += move
            if position == 0:
                answer += 1
        return answer
