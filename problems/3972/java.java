// SPDX-License-Identifier: MIT
// Java adaptation; original Copyright (c) 2018 kamyu104/LeetCode-Solutions.
// Source:
// https://github.com/kamyu104/LeetCode-Solutions/blob/6909130180642cdd7010731c73daecaed3cc772c/C%2B%2B/valid-subarrays-with-matching-sum-digits-ii.cpp
// Changes and license scope: metadata.json, ../../NOTICE.md and ../../LICENSE_SCOPE.md.

// Positive values permit two moving prefix-sum bounds for each decimal length.
// Time: O(n*log(sum(nums))). Space: O(n).
class Solution {
  public long countValidSubarrays(int[] nums, int x) {
    int n = nums.length;
    long[] prefix = new long[n + 1];
    for (int i = 0; i < n; ++i) prefix[i + 1] = prefix[i] + nums[i];
    long answer = 0, total = prefix[n];
    for (long base = 1; base <= total / x; ) {
      long[] count = new long[10];
      int left = 0, right = 0;
      for (int r = 0; r < n; ++r) {
        while (right <= r && prefix[right] <= prefix[r + 1] - x * base)
          ++count[(int) (prefix[right++] % 10)];
        while (left <= r && prefix[left] <= prefix[r + 1] - (x + 1L) * base)
          --count[(int) (prefix[left++] % 10)];
        answer += count[(int) ((prefix[r + 1] - x + 10) % 10)];
      }
      if (base > total / 10) break;
      base *= 10;
    }
    return answer;
  }
}
