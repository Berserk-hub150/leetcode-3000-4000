// SPDX-License-Identifier: MIT
// Java adaptation; original Copyright (c) 2018 kamyu104/LeetCode-Solutions.
// Source:
// https://github.com/kamyu104/LeetCode-Solutions/blob/6909130180642cdd7010731c73daecaed3cc772c/C%2B%2B/maximize-fixed-points-after-deletions.cpp
// Changes and license scope: metadata.json, ../../NOTICE.md and ../../LICENSE_SCOPE.md.

import java.util.*;

class Solution {
  public int maxFixedPoints(int[] nums) {
    List<int[]> pairs = new ArrayList<>();
    for (int i = 0; i < nums.length; i++)
      if (i >= nums[i]) pairs.add(new int[] {i - nums[i], nums[i]});
    pairs.sort((a, b) -> a[0] == b[0] ? Integer.compare(a[1], b[1]) : Integer.compare(a[0], b[0]));
    int[] tails = new int[pairs.size()];
    int length = 0;
    for (int[] pair : pairs) {
      int lo = 0, hi = length;
      while (lo < hi) {
        int mid = (lo + hi) >>> 1;
        if (tails[mid] >= pair[1]) hi = mid;
        else lo = mid + 1;
      }
      tails[lo] = pair[1];
      if (lo == length) length++;
    }
    return length;
  }
}
