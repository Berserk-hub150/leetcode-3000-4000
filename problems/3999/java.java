// SPDX-License-Identifier: MIT
// Java adaptation; original Copyright (c) 2018 kamyu104/LeetCode-Solutions.
// Source:
// https://github.com/kamyu104/LeetCode-Solutions/blob/6909130180642cdd7010731c73daecaed3cc772c/C%2B%2B/minimum-number-of-string-groups-through-transformations.cpp
// Changes and license scope: metadata.json, ../../NOTICE.md and ../../LICENSE_SCOPE.md.

import java.util.*;

// Booth's least rotation independently canonicalizes even and odd positions.
// Time and space: O(total characters).
class Solution {
  private String canonical(String s) {
    int n = s.length(), i = 0, j = 1, k = 0;
    while (i < n && j < n && k < n) {
      char a = s.charAt((i + k) % n), b = s.charAt((j + k) % n);
      if (a == b) {
        ++k;
        continue;
      }
      if (a > b) i += k + 1;
      else j += k + 1;
      if (i == j) ++j;
      k = 0;
    }
    int start = Math.min(i, j);
    return s.substring(start) + s.substring(0, start);
  }

  public int minimumGroups(String[] words) {
    Set<String> groups = new HashSet<>();
    for (String word : words) {
      StringBuilder even = new StringBuilder(), odd = new StringBuilder();
      for (int i = 0; i < word.length(); ++i) (i % 2 == 0 ? even : odd).append(word.charAt(i));
      groups.add(canonical(even.toString()) + "#" + canonical(odd.toString()));
    }
    return groups.size();
  }
}
