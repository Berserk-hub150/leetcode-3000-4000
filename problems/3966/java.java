// SPDX-License-Identifier: MIT
// Java adaptation; original Copyright (c) 2018 kamyu104/LeetCode-Solutions.
// Source:
// https://github.com/kamyu104/LeetCode-Solutions/blob/6909130180642cdd7010731c73daecaed3cc772c/C%2B%2B/count-good-integers-in-a-range.cpp
// Changes and license scope: metadata.json, ../../NOTICE.md and ../../LICENSE_SCOPE.md.

import java.util.*;

// Digit DP. Previous digit 10 means that no nonzero digit has started the number.
// Time: O(log(r)*100). Space: O(log(r)*10).
class Solution {
  private char[] digits;
  private long[][] memo;
  private int limit;

  private long dfs(int position, int previous, boolean tight) {
    if (position == digits.length) return 1;
    if (!tight && memo[position][previous] >= 0) return memo[position][previous];
    int bound = tight ? digits[position] - '0' : 9;
    long result = 0;
    for (int digit = 0; digit <= bound; ++digit) {
      if (previous != 10 && Math.abs(previous - digit) > limit) continue;
      int next = previous == 10 && digit == 0 ? 10 : digit;
      result += dfs(position + 1, next, tight && digit == bound);
    }
    if (!tight) memo[position][previous] = result;
    return result;
  }

  private long count(long bound) {
    if (bound < 0) return 0;
    digits = Long.toString(bound).toCharArray();
    memo = new long[digits.length][11];
    for (long[] row : memo) Arrays.fill(row, -1);
    return dfs(0, 10, true);
  }

  public long goodIntegers(long l, long r, int k) {
    limit = k;
    return count(r) - count(l - 1);
  }
}
