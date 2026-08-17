func maximumSetSize(nums1 []int, nums2 []int) int {
    s1, s2, all := map[int]struct{}{}, map[int]struct{}{}, map[int]struct{}{}
    for _, x := range nums1 { s1[x] = struct{}{}; all[x] = struct{}{} }
    for _, x := range nums2 { s2[x] = struct{}{}; all[x] = struct{}{} }
    half := len(nums1) / 2
    min := func(a, b int) int { if a < b { return a }; return b }
    return min(len(all), min(len(s1), half)+min(len(s2), half))
}
