class Solution:
    def minimumTimeToInitialState(self, word: str, k: int) -> int:
        n = len(word)
        t = 1
        while t * k < n:
            cut = t * k
            if word[cut:] == word[: n - cut]:
                return t
            t += 1
        return t
