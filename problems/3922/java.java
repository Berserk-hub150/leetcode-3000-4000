// SPDX-License-Identifier: MIT
// Java adaptation; original Copyright (c) 2018 kamyu104/LeetCode-Solutions.
// Source:
// https://github.com/kamyu104/LeetCode-Solutions/blob/6909130180642cdd7010731c73daecaed3cc772c/C%2B%2B/minimum-flips-to-make-binary-string-coherent.cpp
// Changes and license scope: metadata.json, ../../NOTICE.md and ../../LICENSE_SCOPE.md.

class Solution {
  public int minFlips(String s) {
    int zeros = 0;
    for (int i = 0; i < s.length(); i++) if (s.charAt(i) == '0') zeros++;
    int ones = s.length() - zeros;
    return Math.min(
        zeros,
        Math.min(
            Math.max(ones - 1, 0),
            Math.max(
                ones - (s.charAt(0) == '1' ? 1 : 0) - (s.charAt(s.length() - 1) == '1' ? 1 : 0),
                0)));
  }
}
