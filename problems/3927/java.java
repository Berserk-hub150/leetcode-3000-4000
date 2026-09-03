// SPDX-License-Identifier: MIT
// Java adaptation; original Copyright (c) 2018 kamyu104/LeetCode-Solutions.
// Source:
// https://github.com/kamyu104/LeetCode-Solutions/blob/6909130180642cdd7010731c73daecaed3cc772c/C%2B%2B/minimize-array-sum-using-divisible-replacements.cpp
// Changes and license scope: metadata.json, ../../NOTICE.md and ../../LICENSE_SCOPE.md.

class Solution {
  public long minArraySum(int[] nums) {
    int max = 0;
    for (int x : nums) max = Math.max(max, x);
    boolean[] present = new boolean[max + 1];
    for (int x : nums) present[x] = true;
    int[] replacement = new int[max + 1];
    for (int x : nums) replacement[x] = x;
    for (int divisor = 1; divisor <= max; divisor++)
      if (present[divisor])
        for (int multiple = divisor * 2; multiple <= max; multiple += divisor)
          if (present[multiple] && replacement[multiple] == multiple)
            replacement[multiple] = divisor;
    long answer = 0;
    for (int x : nums) answer += replacement[x];
    return answer;
  }
}
