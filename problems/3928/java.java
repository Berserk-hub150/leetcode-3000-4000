// SPDX-License-Identifier: MIT
// Java adaptation; original Copyright (c) 2018 kamyu104/LeetCode-Solutions.
// Source:
// https://github.com/kamyu104/LeetCode-Solutions/blob/6909130180642cdd7010731c73daecaed3cc772c/C%2B%2B/minimum-cost-to-buy-apples-ii.cpp
// Changes and license scope: metadata.json, ../../NOTICE.md and ../../LICENSE_SCOPE.md.

import java.util.*;

class Solution {
  public int[] minCost(int n, int[] prices, int[][] roads) {
    List<long[]>[] graph = new List[2 * n];
    for (int i = 0; i < graph.length; i++) graph[i] = new ArrayList<>();
    for (int[] road : roads) {
      int u = road[0], v = road[1];
      long c = road[2], multiplier = road[3];
      graph[u].add(new long[] {v, c});
      graph[v].add(new long[] {u, c});
      graph[u + n].add(new long[] {v + n, c * multiplier});
      graph[v + n].add(new long[] {u + n, c * multiplier});
    }
    for (int i = 0; i < n; i++) graph[i].add(new long[] {i + n, prices[i]});
    int[] answer = new int[n];
    for (int start = 0; start < n; start++) answer[start] = (int) dijkstra(graph, start, start + n);
    return answer;
  }

  private long dijkstra(List<long[]>[] graph, int start, int target) {
    long[] distance = new long[graph.length];
    Arrays.fill(distance, Long.MAX_VALUE);
    distance[start] = 0;
    PriorityQueue<long[]> queue = new PriorityQueue<>(Comparator.comparingLong(a -> a[0]));
    queue.add(new long[] {0, start});
    while (!queue.isEmpty()) {
      long[] current = queue.poll();
      int u = (int) current[1];
      if (current[0] != distance[u]) continue;
      if (u == target) return current[0];
      for (long[] edge : graph[u])
        if (current[0] + edge[1] < distance[(int) edge[0]]) {
          distance[(int) edge[0]] = current[0] + edge[1];
          queue.add(new long[] {distance[(int) edge[0]], edge[0]});
        }
    }
    return Long.MAX_VALUE;
  }
}
