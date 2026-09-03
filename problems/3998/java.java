// SPDX-License-Identifier: MIT
// Java adaptation; original Copyright (c) 2018 kamyu104/LeetCode-Solutions.
// Source:
// https://github.com/kamyu104/LeetCode-Solutions/blob/6909130180642cdd7010731c73daecaed3cc772c/C%2B%2B/transform-binary-string-using-subsequence-sort.cpp
// Changes and license scope: metadata.json, ../../NOTICE.md and ../../LICENSE_SCOPE.md.

import java.util.*;

// Feasible prefix-one-count intervals, intersected with source prefix capacity.
// Time: O(n*m). Space: O(n+m).
class Solution {
  public List<Boolean> transformStr(String s, String[] strs) {
    int[] prefix = new int[s.length() + 1];
    for (int i = 0; i < s.length(); ++i) prefix[i + 1] = prefix[i] + (s.charAt(i) == '1' ? 1 : 0);
    List<Boolean> answer = new ArrayList<>();
    for (String target : strs) {
      int left = 0, right = 0;
      for (int j = 0; j < target.length(); ++j) {
        left += target.charAt(j) == '1' ? 1 : 0;
        right = Math.min(right + (target.charAt(j) != '0' ? 1 : 0), prefix[j + 1]);
        if (left > right) break;
      }
      answer.add(left <= prefix[s.length()] && prefix[s.length()] <= right);
    }
    return answer;
  }
}
