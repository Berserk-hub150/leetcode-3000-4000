class Solution {
    fun maximumSetSize(nums1: IntArray, nums2: IntArray): Int {
        val s1 = nums1.toSet()
        val s2 = nums2.toSet()
        val half = nums1.size / 2
        return minOf((s1 + s2).size, minOf(s1.size, half) + minOf(s2.size, half))
    }
}
