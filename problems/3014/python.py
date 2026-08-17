class Solution:
    def minimumPushes(self, word: str) -> int:
        return sum(i // 8 + 1 for i in range(len(word)))
