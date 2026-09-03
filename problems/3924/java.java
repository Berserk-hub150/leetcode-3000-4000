// SPDX-License-Identifier: MIT
// Java adaptation; original Copyright (c) 2018 kamyu104/LeetCode-Solutions.
// Source:
// https://github.com/kamyu104/LeetCode-Solutions/blob/6909130180642cdd7010731c73daecaed3cc772c/C%2B%2B/minimum-threshold-path-with-limited-heavy-edges.cpp
// Changes and license scope: metadata.json, ../../NOTICE.md and ../../LICENSE_SCOPE.md.

import java.util.*;

class Solution {
  public int minimumThreshold(int n, int[][] edges, int source, int target, int k) {
    List<int[]>[] graph = new List[n];
    for (int i = 0; i < n; i++) graph[i] = new ArrayList<>();
    int[] weights = new int[edges.length + 1];
    int count = 1;
    for (int[] e : edges) {
      graph[e[0]].add(new int[] {e[1], e[2]});
      graph[e[1]].add(new int[] {e[0], e[2]});
      weights[count++] = e[2];
    }
    Arrays.sort(weights);
    int unique = 0;
    for (int w : weights) if (unique == 0 || w != weights[unique - 1]) weights[unique++] = w;
    int lo = 0, hi = unique - 1, answer = -1;
    while (lo <= hi) {
      int mid = (lo + hi) >>> 1;
      if (reachable(graph, source, target, k, weights[mid])) {
        answer = weights[mid];
        hi = mid - 1;
      } else lo = mid + 1;
    }
    return answer;
  }

  private boolean reachable(List<int[]>[] graph, int source, int target, int k, int threshold) {
    int[] distance = new int[graph.length];
    Arrays.fill(distance, Integer.MAX_VALUE);
    distance[source] = 0;
    Deque<Integer> deque = new ArrayDeque<>();
    deque.add(source);
    while (!deque.isEmpty()) {
      int u = deque.pollFirst();
      if (u == target) return distance[u] <= k;
      for (int[] edge : graph[u]) {
        int cost = edge[1] <= threshold ? 0 : 1, next = distance[u] + cost;
        if (next >= distance[edge[0]] || next > k) continue;
        distance[edge[0]] = next;
        if (cost == 0) deque.addFirst(edge[0]);
        else deque.addLast(edge[0]);
      }
    }
    return false;
  }
}
