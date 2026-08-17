from typing import List


class Solution:
    def longestCommonPrefix(self, arr1: List[int], arr2: List[int]) -> int:
        prefixes = set()
        for value in arr1:
            text = str(value)
            for length in range(1, len(text) + 1):
                prefixes.add(text[:length])
        answer = 0
        for value in arr2:
            text = str(value)
            for length in range(1, len(text) + 1):
                if text[:length] in prefixes:
                    answer = max(answer, length)
                else:
                    break
        return answer
