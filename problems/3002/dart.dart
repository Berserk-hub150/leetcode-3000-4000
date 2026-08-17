class Solution {
  int maximumSetSize(List<int> nums1, List<int> nums2) {
    final s1 = nums1.toSet(), s2 = nums2.toSet();
    final all = <int>{...s1, ...s2};
    final half = nums1.length ~/ 2;
    int min2(int a, int b) => a < b ? a : b;
    return min2(all.length, min2(s1.length, half) + min2(s2.length, half));
  }
}
