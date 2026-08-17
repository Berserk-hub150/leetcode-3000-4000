from typing import List


class Solution:
    def countPrefixSuffixPairs(self, words: List[str]) -> int:
        answer = 0
        for j in range(len(words)):
            target = words[j]
            for i in range(j):
                candidate = words[i]
                if target.startswith(candidate) and target.endswith(candidate):
                    answer += 1
        return answer
