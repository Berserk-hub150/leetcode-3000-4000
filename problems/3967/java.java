// SPDX-License-Identifier: MIT
// Java adaptation; original Copyright (c) 2018 kamyu104/LeetCode-Solutions.
// Source:
// https://github.com/kamyu104/LeetCode-Solutions/blob/6909130180642cdd7010731c73daecaed3cc772c/C%2B%2B/finish-time-of-tasks-ii.cpp
// Changes and license scope: metadata.json, ../../NOTICE.md and ../../LICENSE_SCOPE.md.

import java.util.*;

// Two iterative tree passes: subtree values, then rerooted values.
// Time: O(n). Space: O(n).
class Solution {
  public long finishTime(int n, int[][] edges, int[] baseTime) {
    List<Integer>[] graph = new List[n];
    for (int i = 0; i < n; ++i) graph[i] = new ArrayList<>();
    for (int[] edge : edges) {
      graph[edge[0]].add(edge[1]);
      graph[edge[1]].add(edge[0]);
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
    long[] down = new long[n], up = new long[n];
    for (int i = n - 1; i >= 0; --i) {
      int u = order[i];
      long maximum = Long.MIN_VALUE, minimum = Long.MAX_VALUE;
      for (int v : graph[u])
        if (parent[v] == u) {
          maximum = Math.max(maximum, down[v]);
          minimum = Math.min(minimum, down[v]);
        }
      down[u] = baseTime[u] + (minimum == Long.MAX_VALUE ? 0 : 2 * maximum - minimum);
    }
    long answer = Long.MAX_VALUE;
    for (int u : order) {
      long max1 = Long.MIN_VALUE, max2 = max1, min1 = Long.MAX_VALUE, min2 = min1;
      for (int v : graph[u]) {
        long value = v == parent[u] ? up[u] : down[v];
        if (value >= max1) {
          max2 = max1;
          max1 = value;
        } else max2 = Math.max(max2, value);
        if (value <= min1) {
          min2 = min1;
          min1 = value;
        } else min2 = Math.min(min2, value);
      }
      answer = Math.min(answer, baseTime[u] + (graph[u].isEmpty() ? 0 : 2 * max1 - min1));
      for (int v : graph[u])
        if (parent[v] == u) {
          long maximum = down[v] == max1 ? max2 : max1;
          long minimum = down[v] == min1 ? min2 : min1;
          up[v] = baseTime[u] + (graph[u].size() == 1 ? 0 : 2 * maximum - minimum);
        }
    }
    return answer;
  }
}
