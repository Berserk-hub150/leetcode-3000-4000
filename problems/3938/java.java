// SPDX-License-Identifier: MIT
// Java adaptation; original Copyright (c) 2018 kamyu104/LeetCode-Solutions.
// Source:
// https://github.com/kamyu104/LeetCode-Solutions/blob/6909130180642cdd7010731c73daecaed3cc772c/C%2B%2B/maximum-path-intersection-sum-in-a-grid.cpp
// Changes and license scope: metadata.json, ../../NOTICE.md and ../../LICENSE_SCOPE.md.

class Solution {
  public int maxScore(int[][] grid) {
    int n = grid.length, m = grid[0].length, answer = Integer.MIN_VALUE;
    for (int[] row : grid) answer = Math.max(answer, kadane(row));
    for (int c = 0; c < m; c++) {
      int current = grid[0][c] + grid[1][c], best = current;
      for (int r = 2; r < n; r++) {
        current = Math.max(current, grid[r - 1][c]) + grid[r][c];
        best = Math.max(best, current);
      }
      answer = Math.max(answer, best);
    }
    for (int r = 1; r + 1 < n; r++)
      for (int c = 1; c + 1 < m; c++) answer = Math.max(answer, grid[r][c]);
    return answer;
  }

  private int kadane(int[] a) {
    int current = a[0] + a[1], best = current;
    for (int i = 2; i < a.length; i++) {
      current = Math.max(current, a[i - 1]) + a[i];
      best = Math.max(best, current);
    }
    return best;
  }
}
