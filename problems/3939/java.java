// SPDX-License-Identifier: MIT
// Java adaptation; original Copyright (c) 2018 kamyu104/LeetCode-Solutions.
// Source:
// https://github.com/kamyu104/LeetCode-Solutions/blob/6909130180642cdd7010731c73daecaed3cc772c/C%2B%2B/count-non-adjacent-subsets-in-a-rooted-tree.cpp
// Changes and license scope: metadata.json, ../../NOTICE.md and ../../LICENSE_SCOPE.md.

import java.util.*;

class Solution {
  private static final int MOD = 1_000_000_007;
  private List<Integer>[] children;
  private int[] nums;
  private int k;

  public int countValidSubsets(int[] parent, int[] nums, int k) {
    this.k = k;
    int n = nums.length;
    children = new List[n];
    for (int i = 0; i < n; ++i) children[i] = new ArrayList<>();
    for (int i = 1; i < n; ++i) children[parent[i]].add(i);
    int[] order = new int[n];
    int size = 1;
    for (int i = 0; i < size; ++i) for (int v : children[order[i]]) order[size++] = v;
    long[][][] values = new long[n][][];
    for (int t = n - 1; t >= 0; --t) {
      int u = order[t];
      long[][] dp = new long[2][k];
      dp[0][0] = 1;
      dp[1][Math.floorMod(nums[u], k)] = 1;
      for (int v : children[u]) {
        long[][] child = values[v];
        long[] any = new long[k];
        for (int i = 0; i < k; ++i) any[i] = (child[0][i] + child[1][i]) % MOD;
        dp[0] = merge(dp[0], any);
        dp[1] = merge(dp[1], child[0]);
        values[v] = null;
      }
      values[u] = dp;
    }
    return (int) ((values[0][0][0] + values[0][1][0] - 1 + MOD) % MOD);
  }

  private long[] merge(long[] a, long[] b) {
    long[] result = new long[k];
    for (int i = 0; i < k; i++)
      if (a[i] != 0)
        for (int j = 0; j < k; j++)
          if (b[j] != 0) result[(i + j) % k] = (result[(i + j) % k] + a[i] * b[j]) % MOD;
    return result;
  }
}
