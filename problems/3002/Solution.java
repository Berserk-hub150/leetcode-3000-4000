class Solution {
    public int maximumSetSize(int[] nums1, int[] nums2) {
        java.util.Set<Integer> s1 = new java.util.HashSet<>();
        java.util.Set<Integer> s2 = new java.util.HashSet<>();
        for (int x : nums1) s1.add(x);
        for (int x : nums2) s2.add(x);
        java.util.Set<Integer> all = new java.util.HashSet<>(s1);
        all.addAll(s2);
        int half = nums1.length / 2;
        return Math.min(all.size(), Math.min(s1.size(), half) + Math.min(s2.size(), half));
    }
}
