// SPDX-License-Identifier: MIT
// Java adaptation; original Copyright (c) 2018 kamyu104/LeetCode-Solutions.
// Source:
// https://github.com/kamyu104/LeetCode-Solutions/blob/6909130180642cdd7010731c73daecaed3cc772c/C%2B%2B/subarrays-with-xor-at-least-k.cpp
// Changes and license scope: metadata.json, ../../NOTICE.md and ../../LICENSE_SCOPE.md.

class Solution {
  public long countXorSubarrays(int[] nums, int k) {
    int max = Math.max(k, 1);
    for (int x : nums) max = Math.max(max, x);
    int bits = 32 - Integer.numberOfLeadingZeros(max);
    int capacity = 1 + (nums.length + 1) * bits;
    int[] left = new int[capacity], right = new int[capacity], count = new int[capacity];
    int nodes = 0, prefix = 0;
    long answer = 0;
    for (int index = -1; index < nums.length; index++) {
      if (index >= 0) {
        prefix ^= nums[index];
        int cur = 0;
        for (int bit = bits - 1; bit >= 0; bit--) {
          int x = (prefix >>> bit) & 1, threshold = (k >>> bit) & 1;
          if (threshold == 0) {
            int opposite = x == 0 ? right[cur] : left[cur];
            if (opposite != 0) answer += count[opposite];
          }
          cur = (threshold ^ x) == 0 ? left[cur] : right[cur];
          if (cur == 0) break;
          if (bit == 0) answer += count[cur];
        }
      }
      int cur = 0;
      for (int bit = bits - 1; bit >= 0; bit--) {
        if (((prefix >>> bit) & 1) == 0) {
          if (left[cur] == 0) left[cur] = ++nodes;
          cur = left[cur];
        } else {
          if (right[cur] == 0) right[cur] = ++nodes;
          cur = right[cur];
        }
        count[cur]++;
      }
    }
    return answer;
  }
}
