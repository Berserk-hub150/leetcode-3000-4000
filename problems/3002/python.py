from typing import List


class Solution:
    def maximumSetSize(self, nums1: List[int], nums2: List[int]) -> int:
        s1, s2 = set(nums1), set(nums2)
        half = len(nums1) // 2
        return min(len(s1 | s2), min(len(s1), half) + min(len(s2), half))
