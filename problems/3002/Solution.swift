class Solution {
    func maximumSetSize(_ nums1: [Int], _ nums2: [Int]) -> Int {
        let s1 = Set(nums1), s2 = Set(nums2)
        let half = nums1.count / 2
        return min(s1.union(s2).count, min(s1.count, half) + min(s2.count, half))
    }
}
