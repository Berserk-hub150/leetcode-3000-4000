// SPDX-License-Identifier: MIT
// Java adaptation; original Copyright (c) 2018 kamyu104/LeetCode-Solutions.
// Source:
// https://github.com/kamyu104/LeetCode-Solutions/blob/6909130180642cdd7010731c73daecaed3cc772c/C%2B%2B/minimum-adjacent-swaps-to-partition-array.cpp
// Changes and license scope: metadata.json, ../../NOTICE.md and ../../LICENSE_SCOPE.md.

// Count inversions between the three value classes.
// Time: O(n). Space: O(1).
class Solution {
  public int minAdjacentSwaps(int[] nums, int a, int b) {
    final long mod = 1_000_000_007L;
    long answer = 0, middle = 0, high = 0;
    for (int x : nums) {
      if (x < a) answer = (answer + middle + high) % mod;
      else if (x <= b) {
        ++middle;
        answer = (answer + high) % mod;
      } else ++high;
    }
    return (int) answer;
  }
}
