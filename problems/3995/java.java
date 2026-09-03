// SPDX-License-Identifier: MIT
// Java adaptation; original Copyright (c) 2018 kamyu104/LeetCode-Solutions.
// Source:
// https://github.com/kamyu104/LeetCode-Solutions/blob/6909130180642cdd7010731c73daecaed3cc772c/C%2B%2B/minimum-cost-to-convert-string-iii.cpp
// Changes and license scope: metadata.json, ../../NOTICE.md and ../../LICENSE_SCOPE.md.

import java.util.*;

// Prefix DP: unchanged characters or one matching equal-length replacement rule.
// Time: O(n*r*l). Space: O(n).
class Solution {
  public int minCost(String source, String target, String[][] rules, int[] costs) {
    int n = source.length();
    long[] dp = new long[n + 1];
    Arrays.fill(dp, Long.MAX_VALUE);
    dp[0] = 0;
    for (int i = 0; i < n; ++i) {
      if (dp[i] == Long.MAX_VALUE) continue;
      if (source.charAt(i) == target.charAt(i)) dp[i + 1] = Math.min(dp[i + 1], dp[i]);
      for (int j = 0; j < rules.length; ++j) {
        String pattern = rules[j][0], replacement = rules[j][1];
        if (i + pattern.length() > n) continue;
        long cost = costs[j];
        boolean matches = true;
        for (int p = 0; p < pattern.length(); ++p) {
          if (replacement.charAt(p) != target.charAt(i + p)) {
            matches = false;
            break;
          }
          if (pattern.charAt(p) == '*') ++cost;
          else if (pattern.charAt(p) != source.charAt(i + p)) {
            matches = false;
            break;
          }
        }
        if (matches) dp[i + pattern.length()] = Math.min(dp[i + pattern.length()], dp[i] + cost);
      }
    }
    return dp[n] == Long.MAX_VALUE ? -1 : (int) dp[n];
  }
}
