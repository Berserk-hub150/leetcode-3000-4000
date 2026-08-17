from typing import List


class Solution:
    def sumOfEncryptedInt(self, nums: List[int]) -> int:
        total = 0
        for value in nums:
            text = str(value)
            encrypted = int(max(text) * len(text))
            total += encrypted
        return total
