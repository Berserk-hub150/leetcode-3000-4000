// SPDX-License-Identifier: MIT
// Java adaptation; original Copyright (c) 2018 kamyu104/LeetCode-Solutions.
// Source:
// https://github.com/kamyu104/LeetCode-Solutions/blob/6909130180642cdd7010731c73daecaed3cc772c/C%2B%2B/number-of-ways-to-paint-sheets.cpp
// Changes and license scope: metadata.json, ../../NOTICE.md and ../../LICENSE_SCOPE.md.

import java.util.*;

class Solution {
  public int numberOfWays(int n, int[] limit) {
    int[] a = limit.clone();
    for (int i = 0; i < a.length; i++) a[i] = Math.min(a[i], n - 1);
    Arrays.sort(a);
    int m = a.length;
    long[] suffix = new long[m + 1];
    for (int i = m - 1; i >= 0; i--) suffix[i] = suffix[i + 1] + a[i];
    long answer = 0;
    for (int i = 0; i < m; i++) {
      int lo = 0, hi = m;
      while (lo < hi) {
        int mid = (lo + hi) >>> 1;
        if ((long) a[i] + a[mid] >= n) hi = mid;
        else lo = mid + 1;
      }
      long ways = (long) (a[i] - n + 1) * (m - lo) + suffix[lo];
      if (i >= lo) ways -= 2L * a[i] - n + 1;
      answer = (answer + ways) % 1_000_000_007;
    }
    return (int) answer;
  }
}
