// SPDX-License-Identifier: MIT
// Java adaptation; original Copyright (c) 2018 kamyu104/LeetCode-Solutions.
// Source:
// https://github.com/kamyu104/LeetCode-Solutions/blob/6909130180642cdd7010731c73daecaed3cc772c/C%2B%2B/lexicographically-smallest-string-after-reverse-ii.cpp
// Changes and license scope: metadata.json, ../../NOTICE.md and ../../LICENSE_SCOPE.md.

class Solution {
  private static final long MOD = 1_000_000_007L, BASE = 29;
  private String text;
  private long[] forward, backward, powers;

  private long forwardHash(int l, int r) {
    return l > r ? 0 : (forward[r + 1] - forward[l] * powers[r - l + 1] % MOD + MOD) % MOD;
  }

  private long backwardHash(int l, int r) {
    return l > r ? 0 : (backward[l] - backward[r + 1] * powers[r - l + 1] % MOD + MOD) % MOD;
  }

  private long prefixHash(int k, boolean suffix, int length) {
    if (!suffix)
      return length <= k
          ? backwardHash(k - length, k - 1)
          : (backwardHash(0, k - 1) * powers[length - k] + forwardHash(k, length - 1)) % MOD;
    int unchanged = text.length() - k;
    return length <= unchanged
        ? forwardHash(0, length - 1)
        : (forwardHash(0, unchanged - 1) * powers[length - unchanged]
                + backwardHash(text.length() - (length - unchanged), text.length() - 1))
            % MOD;
  }

  private char at(int k, boolean suffix, int index) {
    if (!suffix) return text.charAt(index < k ? k - 1 - index : index);
    int start = text.length() - k;
    return text.charAt(index < start ? index : text.length() - 1 - (index - start));
  }

  private boolean less(int k, boolean suffix, int bestK, boolean bestSuffix) {
    int lo = 0, hi = text.length();
    while (lo < hi) {
      int mid = (lo + hi) >>> 1;
      if (prefixHash(k, suffix, mid + 1) == prefixHash(bestK, bestSuffix, mid + 1)) lo = mid + 1;
      else hi = mid;
    }
    return lo < text.length() && at(k, suffix, lo) < at(bestK, bestSuffix, lo);
  }

  public String lexSmallest(String s) {
    text = s;
    int n = s.length();
    forward = new long[n + 1];
    backward = new long[n + 1];
    powers = new long[n + 1];
    powers[0] = 1;
    for (int i = 0; i < n; i++) {
      forward[i + 1] = (forward[i] * BASE + s.charAt(i)) % MOD;
      powers[i + 1] = powers[i] * BASE % MOD;
    }
    for (int i = n - 1; i >= 0; i--) backward[i] = (backward[i + 1] * BASE + s.charAt(i)) % MOD;
    int bestK = 1;
    boolean bestSuffix = false;
    for (int k = 1; k <= n; k++) {
      if (less(k, false, bestK, bestSuffix)) {
        bestK = k;
        bestSuffix = false;
      }
      if (less(k, true, bestK, bestSuffix)) {
        bestK = k;
        bestSuffix = true;
      }
    }
    StringBuilder answer = new StringBuilder(n);
    for (int i = 0; i < n; i++) answer.append(at(bestK, bestSuffix, i));
    return answer.toString();
  }
}
