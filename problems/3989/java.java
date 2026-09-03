// SPDX-License-Identifier: MIT
// Java adaptation; original Copyright (c) 2018 kamyu104/LeetCode-Solutions.
// Source:
// https://github.com/kamyu104/LeetCode-Solutions/blob/6909130180642cdd7010731c73daecaed3cc772c/C%2B%2B/maximum-consistent-columns-in-a-grid.cpp
// Changes and license scope: metadata.json, ../../NOTICE.md and ../../LICENSE_SCOPE.md.

import java.util.*;

// Intersect per-row compatibility bitsets, then find the longest column chain.
// Time: O(m*(n*log(n)+n^2/64)+n^2). Space: O(n^2/64).
class Solution {
  public int maxConsistentColumns(int[][] grid, int limit) {
    int n = grid[0].length;
    BitSet[] compatible = new BitSet[n];
    for (int i = 0; i < n; ++i) {
      compatible[i] = new BitSet(n);
      compatible[i].set(0, n);
    }
    for (int[] row : grid) {
      Integer[] order = new Integer[n];
      for (int j = 0; j < n; ++j) order[j] = j;
      Arrays.sort(order, Comparator.comparingInt(j -> row[j]));
      BitSet window = new BitSet(n);
      int left = 0, right = 0;
      for (int index : order) {
        while (right < n && (long) row[order[right]] <= (long) row[index] + limit)
          window.set(order[right++]);
        while (left < n && (long) row[order[left]] < (long) row[index] - limit)
          window.clear(order[left++]);
        compatible[index].and(window);
      }
    }
    int[] dp = new int[n];
    int answer = 0;
    for (int j = 0; j < n; ++j) {
      dp[j] = 1;
      for (int i = compatible[j].nextSetBit(0);
          i >= 0 && i < j;
          i = compatible[j].nextSetBit(i + 1)) dp[j] = Math.max(dp[j], dp[i] + 1);
      answer = Math.max(answer, dp[j]);
    }
    return answer;
  }
}
