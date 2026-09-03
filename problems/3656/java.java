// SPDX-License-Identifier: MIT
// Java adaptation; original Copyright (c) 2018 kamyu104/LeetCode-Solutions.
// Source:
// https://github.com/kamyu104/LeetCode-Solutions/blob/6909130180642cdd7010731c73daecaed3cc772c/C%2B%2B/determine-if-a-simple-graph-exists.cpp
// Changes and license scope: metadata.json, ../../NOTICE.md and ../../LICENSE_SCOPE.md.

import java.util.*;

class Solution {
  public boolean simpleGraphExists(int[] degrees) {
    int n = degrees.length;
    int[] d = degrees.clone();
    Arrays.sort(d);
    long[] prefix = new long[n + 1];
    for (int i = 0; i < n; i++) {
      if (d[i] < 0 || d[i] >= n) return false;
      prefix[i + 1] = prefix[i] + d[n - 1 - i];
    }
    if ((prefix[n] & 1) != 0) return false;
    for (int k = 1; k <= n; k++) {
      int lo = k, hi = n;
      while (lo < hi) {
        int mid = (lo + hi) >>> 1;
        if (d[n - 1 - mid] > k) lo = mid + 1;
        else hi = mid;
      }
      long rhs = (long) k * (k - 1) + (long) (lo - k) * k + prefix[n] - prefix[lo];
      if (prefix[k] > rhs) return false;
    }
    return true;
  }
}
