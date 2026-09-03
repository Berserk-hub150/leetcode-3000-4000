// SPDX-License-Identifier: MIT
// Java adaptation; original Copyright (c) 2018 kamyu104/LeetCode-Solutions.
// Source:
// https://github.com/kamyu104/LeetCode-Solutions/blob/6909130180642cdd7010731c73daecaed3cc772c/C%2B%2B/k-th-smallest-remaining-even-integer-in-subarray-queries.cpp
// Changes and license scope: metadata.json, ../../NOTICE.md and ../../LICENSE_SCOPE.md.

class Solution {
  public int[] kthRemainingInteger(int[] nums, int[][] queries) {
    int[] prefix = new int[nums.length + 1], answer = new int[queries.length];
    for (int i = 0; i < nums.length; i++) prefix[i + 1] = prefix[i] + (nums[i] % 2 == 0 ? 1 : 0);
    for (int i = 0; i < queries.length; i++) {
      int l = queries[i][0], r = queries[i][1], k = queries[i][2], lo = l, hi = r;
      while (lo <= hi) {
        int mid = lo + (hi - lo) / 2;
        if (nums[mid] / 2 < (long) k + prefix[mid + 1] - prefix[l]) lo = mid + 1;
        else hi = mid - 1;
      }
      answer[i] = 2 * (k + prefix[hi + 1] - prefix[l]);
    }
    return answer;
  }
}
