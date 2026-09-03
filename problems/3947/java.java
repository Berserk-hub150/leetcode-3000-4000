// SPDX-License-Identifier: MIT
// Java adaptation; original Copyright (c) 2018 kamyu104/LeetCode-Solutions.
// Source:
// https://github.com/kamyu104/LeetCode-Solutions/blob/6909130180642cdd7010731c73daecaed3cc772c/C%2B%2B/maximum-number-of-items-from-sale-ii.cpp
// Changes and license scope: metadata.json, ../../NOTICE.md and ../../LICENSE_SCOPE.md.

import java.util.*;

class Solution {
  public int maximumSaleItems(int[][] items, int budget) {
    int max = 0, minPrice = Integer.MAX_VALUE;
    for (int[] item : items) {
      max = Math.max(max, item[0]);
      minPrice = Math.min(minPrice, item[1]);
    }
    int[] count = new int[max + 1];
    for (int[] item : items) count[item[0]]++;
    int[] multiples = new int[max + 1];
    for (int factor = 1; factor <= max; factor++)
      for (int x = factor; x <= max; x += factor) multiples[factor] += count[x];
    TreeMap<Integer, Long> groups = new TreeMap<>();
    for (int[] item : items)
      if (item[1] < 2L * minPrice) groups.merge(item[1], (long) multiples[item[0]] - 1, Long::sum);
    int answer = 0;
    for (var e : groups.entrySet()) {
      long take = Math.min(budget / e.getKey(), e.getValue());
      answer += 2 * (int) take;
      budget -= take * e.getKey();
      if (budget < e.getKey()) break;
    }
    return answer + budget / minPrice;
  }
}
