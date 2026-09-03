// SPDX-License-Identifier: MIT
// Java adaptation; original Copyright (c) 2018 kamyu104/LeetCode-Solutions.
// Source:
// https://github.com/kamyu104/LeetCode-Solutions/blob/6909130180642cdd7010731c73daecaed3cc772c/C%2B%2B/minimum-operations-to-make-array-modulo-alternating-ii.cpp
// Changes and license scope: metadata.json, ../../NOTICE.md and ../../LICENSE_SCOPE.md.

import java.util.*;

class Solution {
  public long minOperations(int[] nums, int k) {
    int[][] count = new int[2][k];
    for (int i = 0; i < nums.length; i++) count[i & 1][Math.floorMod(nums[i], k)]++;
    long[][] distance = {distances(count[0], k), distances(count[1], k)};
    long[][] best = {bestTwo(distance[0]), bestTwo(distance[1])};
    if (best[0][0] != best[1][0]) return best[0][1] + best[1][1];
    return Math.min(best[0][1] + best[1][3], best[0][3] + best[1][1]);
  }

  private long[] distances(int[] count, int k) {
    int total = 0;
    for (int x : count) total += x;
    long[] d = new long[k];
    int left = 0;
    for (int i = 1; i <= k / 2; i++) left += count[i];
    for (int i = 0; i < k; i++) d[0] += (long) count[i] * Math.min(i, k - i);
    for (int i = 1; i < k; i++) {
      d[i] = d[i - 1] - left + (total - left) - (k % 2 == 1 ? count[(i + k / 2) % k] : 0);
      left += count[(i + k / 2) % k] - count[i];
    }
    return d;
  }

  // index, cost, second index, second cost
  private long[] bestTwo(long[] d) {
    long bi = -1, bc = Long.MAX_VALUE, si = -1, sc = Long.MAX_VALUE;
    for (int i = 0; i < d.length; i++) {
      if (d[i] < bc) {
        si = bi;
        sc = bc;
        bi = i;
        bc = d[i];
      } else if (d[i] < sc) {
        si = i;
        sc = d[i];
      }
    }
    return new long[] {bi, bc, si, sc};
  }
}
