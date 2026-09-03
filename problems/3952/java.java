// SPDX-License-Identifier: MIT
// Java adaptation; original Copyright (c) 2018 kamyu104/LeetCode-Solutions.
// Source:
// https://github.com/kamyu104/LeetCode-Solutions/blob/6909130180642cdd7010731c73daecaed3cc772c/C%2B%2B/maximum-total-value-of-covered-indices.cpp
// Changes and license scope: metadata.json, ../../NOTICE.md and ../../LICENSE_SCOPE.md.

// Time: O(n). Space: O(1).
class Solution {
  public long maxTotal(int[] nums, String s) {
    long answer = 0;
    for (int i = 0; i < nums.length; ) {
      if (s.charAt(i) == '0') {
        ++i;
        continue;
      }
      int minimum = i > 0 ? nums[i - 1] : 0;
      answer += minimum;
      while (i < nums.length && s.charAt(i) == '1') {
        answer += nums[i];
        minimum = Math.min(minimum, nums[i++]);
      }
      answer -= minimum;
    }
    return answer;
  }
}
