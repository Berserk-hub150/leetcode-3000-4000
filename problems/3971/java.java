// SPDX-License-Identifier: MIT
// Java adaptation; original Copyright (c) 2018 kamyu104/LeetCode-Solutions.
// Source:
// https://github.com/kamyu104/LeetCode-Solutions/blob/6909130180642cdd7010731c73daecaed3cc772c/C%2B%2B/maximum-total-value.cpp
// Changes and license scope: metadata.json, ../../NOTICE.md and ../../LICENSE_SCOPE.md.

// Binary search the value of the final selected arithmetic-sequence term.
// Time: O(n*log(max(value))). Space: O(1).
class Solution {
  private static final long MOD = 1_000_000_007L;

  private long[] total(int[] value, int[] decay, long threshold) {
    long count = 0, sum = 0;
    for (int i = 0; i < value.length; ++i)
      if (value[i] >= threshold) {
        long terms = (value[i] - threshold) / decay[i] + 1;
        long ends = 2L * value[i] - (terms - 1) * decay[i];
        count += terms;
        // Divide before multiplication, keeping intermediate products within long.
        long a = terms, b = ends;
        if ((a & 1) == 0) a /= 2;
        else b /= 2;
        sum = (sum + a % MOD * (b % MOD)) % MOD;
      }
    return new long[] {sum, count};
  }

  public int maxTotalValue(int[] value, int[] decay, int m) {
    long[] result = total(value, decay, 1);
    if (result[1] <= m) return (int) result[0];
    long low = 2, high = 0;
    for (int x : value) high = Math.max(high, x);
    while (low < high) {
      long middle = low + (high - low) / 2;
      if (total(value, decay, middle)[1] <= m) high = middle;
      else low = middle + 1;
    }
    result = total(value, decay, low);
    return (int) ((result[0] + (m - result[1]) * (low - 1)) % MOD);
  }
}
