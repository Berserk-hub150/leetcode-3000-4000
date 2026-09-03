// SPDX-License-Identifier: MIT
// Java adaptation; original Copyright (c) 2018 kamyu104/LeetCode-Solutions.
// Source:
// https://github.com/kamyu104/LeetCode-Solutions/blob/6909130180642cdd7010731c73daecaed3cc772c/C%2B%2B/palindromic-subarray-sum.cpp
// Changes and license scope: metadata.json, ../../NOTICE.md and ../../LICENSE_SCOPE.md.

// Manacher's algorithm without sentinel values that could collide with input.
// Time: O(n). Space: O(n). Values are positive, so a center's widest palindrome is best.
class Solution {
  public long getSum(int[] nums) {
    int n = nums.length;
    int[] odd = new int[n], even = new int[n];
    long[] prefix = new long[n + 1];
    for (int i = 0; i < n; ++i) prefix[i + 1] = prefix[i] + nums[i];
    long answer = 0;
    for (int i = 0, left = 0, right = -1; i < n; ++i) {
      int radius = i > right ? 1 : Math.min(odd[left + right - i], right - i + 1);
      while (i - radius >= 0 && i + radius < n && nums[i - radius] == nums[i + radius]) ++radius;
      odd[i] = radius;
      answer = Math.max(answer, prefix[i + radius] - prefix[i - radius + 1]);
      if (i + radius - 1 > right) {
        left = i - radius + 1;
        right = i + radius - 1;
      }
    }
    for (int i = 0, left = 0, right = -1; i < n; ++i) {
      int radius = i > right ? 0 : Math.min(even[left + right - i + 1], right - i + 1);
      while (i - radius - 1 >= 0 && i + radius < n && nums[i - radius - 1] == nums[i + radius])
        ++radius;
      even[i] = radius;
      answer = Math.max(answer, prefix[i + radius] - prefix[i - radius]);
      if (i + radius - 1 > right) {
        left = i - radius;
        right = i + radius - 1;
      }
    }
    return answer;
  }
}
