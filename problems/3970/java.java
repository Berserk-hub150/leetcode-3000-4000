// SPDX-License-Identifier: MIT
// Java adaptation; original Copyright (c) 2018 kamyu104/LeetCode-Solutions.
// Source:
// https://github.com/kamyu104/LeetCode-Solutions/blob/6909130180642cdd7010731c73daecaed3cc772c/C%2B%2B/shortest-path-with-at-most-k-consecutive-identical-characters.cpp
// Changes and license scope: metadata.json, ../../NOTICE.md and ../../LICENSE_SCOPE.md.

import java.util.*;

// Dijkstra on (vertex, current equal-label run length).
// Time: O((n+m)*k*log(n*k)). Space: O(m+n*k).
class Solution {
  public int shortestPath(int n, int[][] edges, String labels, int k) {
    List<int[]>[] graph = new List[n];
    for (int i = 0; i < n; ++i) graph[i] = new ArrayList<>();
    for (int[] edge : edges) graph[edge[0]].add(new int[] {edge[1], edge[2]});
    long[][] distance = new long[n][k];
    for (long[] row : distance) Arrays.fill(row, Long.MAX_VALUE);
    PriorityQueue<long[]> queue = new PriorityQueue<>(Comparator.comparingLong(a -> a[0]));
    distance[0][0] = 0;
    queue.add(new long[] {0, 0, 0});
    while (!queue.isEmpty()) {
      long[] state = queue.remove();
      int u = (int) state[1], run = (int) state[2];
      if (state[0] != distance[u][run]) continue;
      if (u == n - 1) return (int) state[0];
      for (int[] edge : graph[u]) {
        int v = edge[0], next = labels.charAt(u) == labels.charAt(v) ? run + 1 : 0;
        if (next >= k) continue;
        long candidate = state[0] + edge[1];
        if (candidate < distance[v][next]) {
          distance[v][next] = candidate;
          queue.add(new long[] {candidate, v, next});
        }
      }
    }
    return -1;
  }
}
