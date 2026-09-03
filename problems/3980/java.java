// SPDX-License-Identifier: MIT
// Java adaptation; original Copyright (c) 2018 kamyu104/LeetCode-Solutions.
// Source:
// https://github.com/kamyu104/LeetCode-Solutions/blob/6909130180642cdd7010731c73daecaed3cc772c/C%2B%2B/minimum-operations-to-transform-binary-string.cpp
// Changes and license scope: metadata.json, ../../NOTICE.md and ../../LICENSE_SCOPE.md.

// Time: O(n). Space: O(n) for a mutable character array.
class Solution {
  public int minOperations(String s1, String s2) {
    if (s1.equals("1") && s2.equals("0")) return -1;
    char[] current = s1.toCharArray();
    int answer = 0;
    for (int i = 0; i < current.length; ++i) {
      if (current[i] == s2.charAt(i)) continue;
      if (current[i] == '0') ++answer;
      else if (i + 1 < current.length) {
        answer += current[i + 1] == '1' ? 1 : 2;
        current[i + 1] = '0';
      } else answer += 2;
    }
    return answer;
  }
}
