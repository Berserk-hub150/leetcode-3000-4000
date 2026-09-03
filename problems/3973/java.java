// SPDX-License-Identifier: MIT
// Java adaptation; original Copyright (c) 2018 kamyu104/LeetCode-Solutions.
// Source:
// https://github.com/kamyu104/LeetCode-Solutions/blob/6909130180642cdd7010731c73daecaed3cc772c/C%2B%2B/distinct-gate-paths-to-lca.cpp
// Changes and license scope: metadata.json, ../../NOTICE.md and ../../LICENSE_SCOPE.md.

import java.util.*;

// Binary lifting with 2x2 transition matrices on upward paths.
// Time: O((n+q)*log(n)). Space: O(n*log(n)).
class Solution {
  private static final long MOD = 1_000_000_007L;
  private int[][] ancestor;
  private long[][][] transition;
  private int[] depth;

  private long[] multiply(long[] a, long[] b) {
    return new long[] {
      (a[0] * b[0] + a[1] * b[2]) % MOD,
      (a[0] * b[1] + a[1] * b[3]) % MOD,
      (a[2] * b[0] + a[3] * b[2]) % MOD,
      (a[2] * b[1] + a[3] * b[3]) % MOD
    };
  }

  private int lca(int a, int b) {
    if (depth[a] < depth[b]) {
      int t = a;
      a = b;
      b = t;
    }
    int difference = depth[a] - depth[b];
    for (int bit = 0; bit < ancestor.length; ++bit)
      if ((difference & (1 << bit)) != 0) a = ancestor[bit][a];
    if (a == b) return a;
    for (int bit = ancestor.length - 1; bit >= 0; --bit)
      if (ancestor[bit][a] != ancestor[bit][b]) {
        a = ancestor[bit][a];
        b = ancestor[bit][b];
      }
    return ancestor[0][a];
  }

  private long count(int u, int card, int target) {
    long blue = card == 0 ? 1 : 0, red = card == 1 ? 1 : 0;
    int difference = depth[u] - depth[target];
    for (int bit = 0; bit < ancestor.length; ++bit)
      if ((difference & (1 << bit)) != 0) {
        long[] matrix = transition[bit][u];
        long nextBlue = (blue * matrix[0] + red * matrix[2]) % MOD;
        red = (blue * matrix[1] + red * matrix[3]) % MOD;
        blue = nextBlue;
        u = ancestor[bit][u];
      }
    return (blue + red) % MOD;
  }

  public int distinctPaths(int n, int[] parent, int[][] gates, int[][] queries) {
    int levels = 32 - Integer.numberOfLeadingZeros(Math.max(1, n));
    ancestor = new int[levels][n];
    transition = new long[levels][n][];
    depth = new int[n];
    List<Integer>[] children = new List[n];
    for (int i = 0; i < n; ++i) children[i] = new ArrayList<>();
    int root = 0;
    for (int u = 0; u < n; ++u) {
      if (parent[u] >= 0) children[parent[u]].add(u);
      else root = u;
      ancestor[0][u] = parent[u];
      transition[0][u] = new long[] {gates[u][1], gates[u][2], gates[u][2], gates[u][0]};
    }
    ArrayDeque<Integer> queue = new ArrayDeque<>();
    queue.add(root);
    while (!queue.isEmpty()) {
      int u = queue.remove();
      for (int v : children[u]) {
        depth[v] = depth[u] + 1;
        queue.add(v);
      }
    }
    for (int bit = 1; bit < levels; ++bit) {
      Arrays.fill(ancestor[bit], -1);
      for (int u = 0; u < n; ++u) {
        int middle = ancestor[bit - 1][u];
        if (middle < 0) continue;
        ancestor[bit][u] = ancestor[bit - 1][middle];
        if (transition[bit - 1][middle] != null)
          transition[bit][u] = multiply(transition[bit - 1][u], transition[bit - 1][middle]);
      }
    }
    int answer = 0;
    for (int[] q : queries) {
      int common = lca(q[0], q[2]);
      answer ^= (int) (count(q[0], q[1], common) * count(q[2], q[3], common) % MOD);
    }
    return answer;
  }
}
