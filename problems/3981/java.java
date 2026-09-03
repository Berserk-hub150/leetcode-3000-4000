// SPDX-License-Identifier: MIT
// Java adaptation; original Copyright (c) 2018 kamyu104/LeetCode-Solutions.
// Source:
// https://github.com/kamyu104/LeetCode-Solutions/blob/6909130180642cdd7010731c73daecaed3cc772c/C%2B%2B/count-distinct-ways-to-form-target-from-two-strings.cpp
// Changes and license scope: metadata.json, ../../NOTICE.md and ../../LICENSE_SCOPE.md.

// DP with row/column prefix sums; both input words must contribute.
// Time: O(n*m*t). Space: O(n*m).
class Solution {
  public int interleaveCharacters(String word1, String word2, String target) {
    final int mod = 1_000_000_007;
    int n = word1.length(), m = word2.length();
    int[][] dp = new int[n + 1][m + 1];
    dp[0][0] = 1;
    for (char c : target.toCharArray()) {
      int[][] next = new int[n + 1][m + 1];
      int[] column = new int[m + 1];
      for (int i = 0; i <= n; ++i) {
        int row = 0;
        for (int j = 0; j <= m; ++j) {
          row = (row + dp[i][j]) % mod;
          if (j < m && word2.charAt(j) == c) next[i][j + 1] = (next[i][j + 1] + row) % mod;
          column[j] = (column[j] + dp[i][j]) % mod;
          if (i < n && word1.charAt(i) == c) next[i + 1][j] = (next[i + 1][j] + column[j]) % mod;
        }
      }
      dp = next;
    }
    int answer = 0;
    for (int i = 1; i <= n; ++i) for (int j = 1; j <= m; ++j) answer = (answer + dp[i][j]) % mod;
    return answer;
  }
}
