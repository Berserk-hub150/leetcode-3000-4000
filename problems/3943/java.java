// SPDX-License-Identifier: MIT
// Java adaptation; original Copyright (c) 2018 kamyu104/LeetCode-Solutions.
// Source:
// https://github.com/kamyu104/LeetCode-Solutions/blob/6909130180642cdd7010731c73daecaed3cc772c/C%2B%2B/number-of-pairs-after-increment.cpp
// Changes and license scope: metadata.json, ../../NOTICE.md and ../../LICENSE_SCOPE.md.

import java.util.*;

class Solution {
  public int[] numberOfPairs(int[] nums1, int[] nums2, int[][] queries) {
    Map<Long, Integer> first = new HashMap<>();
    for (int x : nums1) first.merge((long) x, 1, Integer::sum);
    long[] values = new long[nums2.length];
    for (int i = 0; i < values.length; i++) values[i] = nums2[i];
    int block = Math.max(1, (int) Math.sqrt((long) first.size() * values.length) + 1),
        blocks = (values.length + block - 1) / block;
    List<Map<Long, Integer>> counts = new ArrayList<>();
    long[] lazy = new long[blocks];
    for (int b = 0; b < blocks; b++) {
      Map<Long, Integer> map = new HashMap<>();
      for (int i = b * block; i < Math.min(values.length, (b + 1) * block); i++)
        map.merge(values[i], 1, Integer::sum);
      counts.add(map);
    }
    int[] out = new int[queries.length];
    int used = 0;
    for (int[] q : queries) {
      if (q[0] == 2) {
        long total = 0;
        for (var e : first.entrySet())
          for (int b = 0; b < blocks; b++)
            total +=
                (long) e.getValue() * counts.get(b).getOrDefault(q[1] - e.getKey() - lazy[b], 0);
        out[used++] = (int) total;
        continue;
      }
      int left = q[1], right = q[2], delta = q[3];
      if (left / block == right / block)
        update(values, counts.get(left / block), left, right, delta);
      else {
        update(values, counts.get(left / block), left, (left / block + 1) * block - 1, delta);
        for (int b = left / block + 1; b < right / block; b++) lazy[b] += delta;
        update(values, counts.get(right / block), (right / block) * block, right, delta);
      }
    }
    return Arrays.copyOf(out, used);
  }

  private void update(long[] a, Map<Long, Integer> count, int left, int right, int delta) {
    for (int i = left; i <= right; i++) {
      long old = a[i];
      count.compute(old, (k, v) -> v == null || v == 1 ? null : v - 1);
      a[i] += delta;
      count.merge(a[i], 1, Integer::sum);
    }
  }
}
