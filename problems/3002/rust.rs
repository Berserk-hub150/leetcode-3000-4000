impl Solution {
    pub fn maximum_set_size(nums1: Vec<i32>, nums2: Vec<i32>) -> i32 {
        use std::collections::HashSet;
        let half = nums1.len() / 2;
        let s1: HashSet<i32> = nums1.into_iter().collect();
        let s2: HashSet<i32> = nums2.into_iter().collect();
        let union = s1.union(&s2).count();
        union.min(s1.len().min(half) + s2.len().min(half)) as i32
    }
}
