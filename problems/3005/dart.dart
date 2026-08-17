class Solution {
  int maxFrequencyElements(List<int> nums) {
    final freq = <int, int>{};
    var best = 0;
    for (final x in nums) {
      final count = (freq[x] ?? 0) + 1;
      freq[x] = count;
      if (count > best) best = count;
    }
    var ans = 0;
    for (final count in freq.values) {
      if (count == best) ans += count;
    }
    return ans;
  }
}
