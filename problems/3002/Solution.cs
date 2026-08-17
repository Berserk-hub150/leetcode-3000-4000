public class Solution {
    public int MaximumSetSize(int[] nums1, int[] nums2) {
        var s1 = new System.Collections.Generic.HashSet<int>(nums1);
        var s2 = new System.Collections.Generic.HashSet<int>(nums2);
        var all = new System.Collections.Generic.HashSet<int>(s1);
        all.UnionWith(s2);
        int half = nums1.Length / 2;
        return System.Math.Min(all.Count, System.Math.Min(s1.Count, half) + System.Math.Min(s2.Count, half));
    }
}
