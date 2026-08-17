object Solution {
    def maximumSetSize(nums1: Array[Int], nums2: Array[Int]): Int = {
        val s1 = nums1.toSet
        val s2 = nums2.toSet
        val half = nums1.length / 2
        math.min((s1 union s2).size, math.min(s1.size, half) + math.min(s2.size, half))
    }
}
