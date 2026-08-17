from collections import Counter
from typing import List


class Solution:
    def maxPalindromesAfterOperations(self, words: List[str]) -> int:
        frequencies = Counter("".join(words))
        pairs = sum(v // 2 for v in frequencies.values())
        answer = 0
        for length in sorted(map(len, words)):
            required = length // 2
            if required > pairs:
                break
            pairs -= required
            answer += 1
        return answer
