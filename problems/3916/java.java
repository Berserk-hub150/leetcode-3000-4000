// SPDX-License-Identifier: MIT
// Java adaptation; original Copyright (c) 2018 kamyu104/LeetCode-Solutions.
// Source:
// https://github.com/kamyu104/LeetCode-Solutions/blob/6909130180642cdd7010731c73daecaed3cc772c/C%2B%2B/number-of-zigzag-arrays-iii.cpp
// Changes and license scope: metadata.json, ../../NOTICE.md and ../../LICENSE_SCOPE.md.

class Solution {
  private static final long MOD = 1_000_000_007L;

  private long pow(long x, long n) {
    long ans = 1;
    for (; n > 0; n >>= 1, x = x * x % MOD) if ((n & 1) != 0) ans = ans * x % MOD;
    return ans;
  }

  private long count(int n, int width) {
    long[] dp = new long[width];
    for (int i = 0; i < width; i++) dp[i] = i;
    for (int step = 0; step < n - 2; step++) {
      long[] next = new long[width];
      for (int i = 0; i + 1 < width; i++) next[i + 1] = (next[i] + dp[width - 1 - i]) % MOD;
      dp = next;
    }
    long total = 0;
    for (long x : dp) total = (total + x) % MOD;
    return total * 2 % MOD;
  }

  public int zigZagArrays(int n, int l, int r) {
    int width = r - l + 1;
    if (n == 1) return width;
    if (width <= n + 1) return (int) count(n, width);
    long[] inverseFactorial = new long[n + 1];
    long factorial = 1;
    for (int i = 1; i <= n; i++) factorial = factorial * i % MOD;
    inverseFactorial[n] = pow(factorial, MOD - 2);
    for (int i = n; i > 0; i--) inverseFactorial[i - 1] = inverseFactorial[i] * i % MOD;
    long[] prefix = new long[n + 2], suffix = new long[n + 2];
    prefix[0] = suffix[n + 1] = 1;
    for (int i = 0; i <= n; i++) prefix[i + 1] = prefix[i] * (width - 1L - i) % MOD;
    for (int i = n; i >= 0; i--) suffix[i] = suffix[i + 1] * (width - 1L - i) % MOD;
    long answer = 0;
    for (int i = 0; i <= n; i++) {
      long term =
          count(n, i + 1)
              * prefix[i]
              % MOD
              * suffix[i + 1]
              % MOD
              * inverseFactorial[i]
              % MOD
              * inverseFactorial[n - i]
              % MOD;
      answer = (answer + ((n - i) % 2 == 0 ? term : MOD - term)) % MOD;
    }
    return (int) answer;
  }
}
