// SPDX-License-Identifier: MIT
// Java adaptation; original Copyright (c) 2018 kamyu104/LeetCode-Solutions.
// Source:
// https://github.com/kamyu104/LeetCode-Solutions/blob/6909130180642cdd7010731c73daecaed3cc772c/C%2B%2B/once-twice.cpp
// Changes and license scope: metadata.json, ../../NOTICE.md and ../../LICENSE_SCOPE.md.

class Solution {
  public int[] onceTwice(int[] nums) {
    int[] dp = {-1, 0, 0};
    for (int x : nums) {
      int[] next = new int[3];
      for (int i = 0; i < 3; i++) next[i] = (x & dp[(i + 2) % 3]) | (~x & dp[i]);
      dp = next;
    }
    int[] part = {-1, 0, 0};
    for (int x : nums) {
      if ((~x & dp[1]) != 0 || (x & dp[2]) != 0) continue;
      int[] next = new int[3];
      for (int i = 0; i < 3; i++) next[i] = (x & part[(i + 2) % 3]) | (~x & part[i]);
      part = next;
    }
    return new int[] {part[1], (part[1] ^ dp[1]) | dp[2]};
  }
}
