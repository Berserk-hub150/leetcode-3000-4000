// SPDX-License-Identifier: MIT
// Java adaptation; original Copyright (c) 2018 kamyu104/LeetCode-Solutions.
// Source:
// https://github.com/kamyu104/LeetCode-Solutions/blob/6909130180642cdd7010731c73daecaed3cc772c/C%2B%2B/create-grid-with-exactly-k-paths-i.cpp
// Changes and license scope: metadata.json, ../../NOTICE.md and ../../LICENSE_SCOPE.md.

import java.util.*;

// Embed a small k-path pattern, then extend its exit corridor.
// Time and output space: O(m*n).
class Solution {
  public List<String> createGrid(int m, int n, int k) {
    String[][][] patterns = {
      {},
      {{"."}},
      {{"..", ".."}},
      {{"..", "..", ".."}, {"...", "..."}},
      {{"..", "..", "..", ".."}, {"....", "...."}, {"..#", "...", "#.."}}
    };
    for (String[] pattern : patterns[k]) {
      int height = pattern.length, width = pattern[0].length();
      if (height > m || width > n) continue;
      char[][] grid = new char[m][n];
      for (char[] row : grid) Arrays.fill(row, '#');
      for (int i = 0; i < height; ++i)
        for (int j = 0; j < width; ++j) grid[i][j] = pattern[i].charAt(j);
      for (int i = height; i < m; ++i) grid[i][width - 1] = '.';
      for (int j = width; j < n; ++j) grid[m - 1][j] = '.';
      List<String> answer = new ArrayList<>();
      for (char[] row : grid) answer.add(new String(row));
      return answer;
    }
    return new ArrayList<>();
  }
}
