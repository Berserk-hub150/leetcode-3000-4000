class Solution:
    def countKeyChanges(self, s: str) -> int:
        lowered = s.lower()
        return sum(lowered[i] != lowered[i - 1] for i in range(1, len(lowered)))
