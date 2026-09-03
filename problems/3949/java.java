// SPDX-License-Identifier: MIT
// Java adaptation; original Copyright (c) 2018 kamyu104/LeetCode-Solutions.
// Source:
// https://github.com/kamyu104/LeetCode-Solutions/blob/6909130180642cdd7010731c73daecaed3cc772c/C%2B%2B/subtree-inversion-sum-ii.cpp
// Changes and license scope: metadata.json, ../../NOTICE.md and ../../LICENSE_SCOPE.md.

import java.util.*;

// Tree DP with distance states; iterative traversal avoids a deep Java call stack.
// Time: O(n*k). Space: O(n*k).
class Solution {
  public int subtreeInversionSum(int[][] edges, int[] nums, int k) {
    int n = nums.length;
    List<Integer>[] graph = new List[n];
    for (int i = 0; i < n; ++i) graph[i] = new ArrayList<>();
    for (int[] e : edges) {
      graph[e[0]].add(e[1]);
      graph[e[1]].add(e[0]);
    }
    int[] parent = new int[n], order = new int[n];
    Arrays.fill(parent, -1);
    int size = 1;
    for (int i = 0; i < size; ++i) {
      int u = order[i];
      for (int v : graph[u])
        if (v != parent[u]) {
          parent[v] = u;
          order[size++] = v;
        }
    }
    long[][] maximum = new long[n][], minimum = new long[n][];
    for (int t = n - 1; t >= 0; --t) {
      int u = order[t];
      long[] hi = new long[k], lo = new long[k];
      Arrays.fill(hi, nums[u]);
      Arrays.fill(lo, nums[u]);
      for (int v : graph[u])
        if (parent[v] == u) {
          long[] childHi = maximum[v], childLo = minimum[v];
          for (int i = 0; i < k / 2; ++i) {
            hi[i] = Math.max(hi[i] + childHi[k - 2 - i], hi[k - 2 - i] + childHi[i]);
            lo[i] = Math.min(lo[i] + childLo[k - 2 - i], lo[k - 2 - i] + childLo[i]);
          }
          for (int i = k / 2; i < k; ++i) {
            hi[i] += childHi[i];
            lo[i] += childLo[i];
          }
          for (int i = k - 2; i >= 0; --i) {
            hi[i] = Math.max(hi[i], hi[i + 1]);
            lo[i] = Math.min(lo[i], lo[i + 1]);
          }
          maximum[v] = minimum[v] = null;
        }
      long best = Math.max(hi[0], -lo[k - 1]);
      long worst = Math.min(lo[0], -hi[k - 1]);
      for (int i = k - 1; i > 0; --i) {
        hi[i] = hi[i - 1];
        lo[i] = lo[i - 1];
      }
      hi[0] = best;
      lo[0] = worst;
      maximum[u] = hi;
      minimum[u] = lo;
    }
    return (int) maximum[0][0];
  }
}
