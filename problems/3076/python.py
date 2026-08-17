from typing import List


class Solution:
    def shortestSubstrings(self, arr: List[str]) -> List[str]:
        answer = []
        for i, word in enumerate(arr):
            best = ""
            for length in range(1, len(word) + 1):
                candidates = set()
                for start in range(len(word) - length + 1):
                    sub = word[start:start + length]
                    if all(sub not in arr[j] for j in range(len(arr)) if j != i):
                        candidates.add(sub)
                if candidates:
                    best = min(candidates)
                    break
            answer.append(best)
        return answer
