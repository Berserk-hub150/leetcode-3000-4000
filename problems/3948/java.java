// SPDX-License-Identifier: MIT
// Java adaptation; original Copyright (c) 2018 kamyu104/LeetCode-Solutions.
// Source:
// https://github.com/kamyu104/LeetCode-Solutions/blob/6909130180642cdd7010731c73daecaed3cc772c/C%2B%2B/lexicographically-maximum-mex-array.cpp
// Changes and license scope: metadata.json, ../../NOTICE.md and ../../LICENSE_SCOPE.md.

import java.util.*;

// Greedily finish each block when it reaches the MEX of the remaining suffix.
// Time: O(n). Space: O(n).
class Solution {
  public int[] maximumMEX(int[] nums) {
    int n = nums.length;
    int[] seen = new int[n + 1], suffix = new int[n];
    Arrays.fill(seen, -1);
    int mex = 0;
    for (int i = n - 1; i >= 0; --i) {
      if (nums[i] <= n) seen[nums[i]] = 0;
      while (seen[mex] == 0) ++mex;
      suffix[i] = mex;
    }
    int[] answer = new int[n];
    int size = 0, start = 0, generation = 1;
    mex = 0;
    for (int i = 0; i < n && suffix[start] != 0; ++i) {
      if (nums[i] <= n) seen[nums[i]] = generation;
      while (seen[mex] == generation) ++mex;
      if (mex == suffix[start]) {
        answer[size++] = mex;
        ++generation;
        mex = 0;
        start = i + 1;
      }
    }
    return Arrays.copyOf(answer, size + n - start);
  }
}
