// SPDX-License-Identifier: MIT
// Java adaptation; original Copyright (c) 2018 kamyu104/LeetCode-Solutions.
// Source:
// https://github.com/kamyu104/LeetCode-Solutions/blob/6909130180642cdd7010731c73daecaed3cc772c/C%2B%2B/create-grid-with-exactly-k-paths-ii.cpp
// Changes and license scope: metadata.json, ../../NOTICE.md and ../../LICENSE_SCOPE.md.

import java.util.*;

// A chain of 2x2 blocks doubles the number of paths; set bits open exits.
// Time and output space: O(log(k)^2).
class Solution {
  public List<String> createGrid(int k) {
    int length = 32 - Integer.numberOfLeadingZeros(k);
    int rows = 2 * length, columns = length + 3;
    char[][] grid = new char[rows][columns];
    for (char[] row : grid) Arrays.fill(row, '#');
    for (int i = 0; i < length; ++i) {
      int r = 2 * i;
      grid[r][i] = grid[r][i + 1] = grid[r + 1][i] = grid[r + 1][i + 1] = '.';
      if ((k & (1 << i)) != 0) for (int c = i + 2; c < columns; ++c) grid[r][c] = '.';
    }
    for (char[] row : grid) row[columns - 1] = '.';
    List<String> answer = new ArrayList<>();
    for (char[] row : grid) answer.add(new String(row));
    return answer;
  }
}
