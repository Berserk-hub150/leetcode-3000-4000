// SPDX-License-Identifier: MIT
// Java adaptation; original Copyright (c) 2018 kamyu104/LeetCode-Solutions.
// Source:
// https://github.com/kamyu104/LeetCode-Solutions/blob/6909130180642cdd7010731c73daecaed3cc772c/C%2B%2B/smallest-unique-subarray.cpp
// Changes and license scope: metadata.json, ../../NOTICE.md and ../../LICENSE_SCOPE.md.

import java.util.*;

class Solution {
  private static final long M1 = 1_000_000_007L, M2 = 1_000_000_009L, B = 1_000_003L;

  public int smallestUniqueSubarray(int[] nums) {
    int lo = 1, hi = nums.length;
    while (lo < hi) {
      int mid = (lo + hi) >>> 1;
      if (hasUnique(nums, mid)) hi = mid;
      else lo = mid + 1;
    }
    return lo;
  }

  private boolean hasUnique(int[] a, int length) {
    int n = a.length;
    long[] h1 = new long[n + 1], h2 = new long[n + 1], p1 = new long[n + 1], p2 = new long[n + 1];
    p1[0] = p2[0] = 1;
    for (int i = 0; i < n; i++) {
      long x = a[i] + 1_000_000_001L;
      h1[i + 1] = (h1[i] * B + x) % M1;
      h2[i + 1] = (h2[i] * B + x) % M2;
      p1[i + 1] = p1[i] * B % M1;
      p2[i + 1] = p2[i] * B % M2;
    }
    Map<Long, Integer> count = new HashMap<>();
    for (int i = 0; i + length <= n; i++) {
      long x = (h1[i + length] - h1[i] * p1[length] % M1 + M1) % M1,
          y = (h2[i + length] - h2[i] * p2[length] % M2 + M2) % M2,
          key = (x << 32) ^ y;
      count.merge(key, 1, Integer::sum);
    }
    for (int c : count.values()) if (c == 1) return true;
    return false;
  }
}
