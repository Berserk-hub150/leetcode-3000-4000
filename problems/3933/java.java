// SPDX-License-Identifier: MIT
// Java adaptation; original Copyright (c) 2018 kamyu104/LeetCode-Solutions.
// Source:
// https://github.com/kamyu104/LeetCode-Solutions/blob/6909130180642cdd7010731c73daecaed3cc772c/C%2B%2B/largest-local-values-in-a-matrix-ii.cpp
// Changes and license scope: metadata.json, ../../NOTICE.md and ../../LICENSE_SCOPE.md.

class Solution {
  public int countLocalMaximums(int[][] matrix) {
    Sparse2D sparse = new Sparse2D(matrix);
    int n = matrix.length, m = matrix[0].length, answer = 0;
    for (int r = 0; r < n; r++)
      for (int c = 0; c < m; c++) {
        int x = matrix[r][c];
        if (x == 0) continue;
        int r1 = Math.max(0, r - x),
            r2 = Math.min(n - 1, r + x),
            c1 = Math.max(0, c - x),
            c2 = Math.min(m - 1, c + x);
        boolean tl = r - x >= 0 && c - x >= 0,
            tr = r - x >= 0 && c + x < m,
            bl = r + x < n && c - x >= 0,
            br = r + x < n && c + x < m;
        int a = sparse.query(r1, c1 + (tl || bl ? 1 : 0), r2, c2 - (tr || br ? 1 : 0));
        int b = sparse.query(r1 + (tl || tr ? 1 : 0), c1, r2 - (bl || br ? 1 : 0), c2);
        if (Math.max(a, b) <= x) answer++;
      }
    return answer;
  }

  private static class Sparse2D {
    int[][][][] table;
    int[] logs;

    Sparse2D(int[][] a) {
      int n = a.length, m = a[0].length;
      logs = new int[Math.max(n, m) + 1];
      for (int i = 2; i < logs.length; i++) logs[i] = logs[i / 2] + 1;
      int ln = logs[n] + 1, lm = logs[m] + 1;
      table = new int[ln][lm][n][m];
      for (int r = 0; r < n; r++) System.arraycopy(a[r], 0, table[0][0][r], 0, m);
      for (int j = 1; j < lm; j++)
        for (int r = 0; r < n; r++)
          for (int c = 0; c + (1 << j) <= m; c++)
            table[0][j][r][c] =
                Math.max(table[0][j - 1][r][c], table[0][j - 1][r][c + (1 << (j - 1))]);
      for (int i = 1; i < ln; i++)
        for (int j = 0; j < lm; j++)
          for (int r = 0; r + (1 << i) <= n; r++)
            for (int c = 0; c + (1 << j) <= m; c++)
              table[i][j][r][c] =
                  Math.max(table[i - 1][j][r][c], table[i - 1][j][r + (1 << (i - 1))][c]);
    }

    int query(int r1, int c1, int r2, int c2) {
      if (r1 > r2 || c1 > c2) return Integer.MIN_VALUE;
      int i = logs[r2 - r1 + 1],
          j = logs[c2 - c1 + 1],
          rr = r2 - (1 << i) + 1,
          cc = c2 - (1 << j) + 1;
      return Math.max(
          Math.max(table[i][j][r1][c1], table[i][j][r1][cc]),
          Math.max(table[i][j][rr][c1], table[i][j][rr][cc]));
    }
  }
}
