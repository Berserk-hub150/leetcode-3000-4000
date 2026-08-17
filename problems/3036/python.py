from typing import List


class Solution:
    def countMatchingSubarrays(self, nums: List[int], pattern: List[int]) -> int:
        text = []
        for a, b in zip(nums, nums[1:]):
            text.append(1 if b > a else -1 if b < a else 0)

        pi = [0] * len(pattern)
        for i in range(1, len(pattern)):
            j = pi[i - 1]
            while j and pattern[i] != pattern[j]:
                j = pi[j - 1]
            if pattern[i] == pattern[j]:
                j += 1
            pi[i] = j

        answer = 0
        j = 0
        for value in text:
            while j and value != pattern[j]:
                j = pi[j - 1]
            if value == pattern[j]:
                j += 1
            if j == len(pattern):
                answer += 1
                j = pi[j - 1]
        return answer
