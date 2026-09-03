// SPDX-License-Identifier: MIT
// Java adaptation; original Copyright (c) 2018 kamyu104/LeetCode-Solutions.
// Source:
// https://github.com/kamyu104/LeetCode-Solutions/blob/6909130180642cdd7010731c73daecaed3cc772c/C%2B%2B/maximum-subarray-sum-after-at-most-k-swaps.cpp
// Changes and license scope: metadata.json, ../../NOTICE.md and ../../LICENSE_SCOPE.md.

import java.util.*;

// Enumerate the kept interval, maintaining the k best removals and outside values.
// Time: O(n^2*log(k+1)). Space: O(n+k).
class Solution {
  private long insert(PriorityQueue<Long> heap, long value, long total, int k) {
    if (k == 0) return total;
    heap.add(value);
    total += value;
    if (heap.size() > k) total -= heap.remove();
    return total;
  }

  public long maxSum(int[] nums, int k) {
    int n = nums.length, negatives = 0, maximum = nums[0];
    long positiveSum = 0;
    long[] prefix = new long[n + 1];
    for (int i = 0; i < n; ++i) {
      maximum = Math.max(maximum, nums[i]);
      if (nums[i] < 0) ++negatives;
      else positiveSum += nums[i];
      prefix[i + 1] = prefix[i] + nums[i];
    }
    if (maximum < 0) return maximum;
    if (negatives <= k) return positiveSum;
    long answer = 0;
    for (int start = 0; start < n; ++start) {
      PriorityQueue<Long> removed = new PriorityQueue<>(), outside = new PriorityQueue<>();
      long[] benefit = new long[n];
      long total = 0;
      for (int end = start; end < n; ++end) {
        if (nums[end] < 0) total = insert(removed, -(long) nums[end], total, k);
        benefit[end] = total;
      }
      total = 0;
      for (int i = 0; i < start; ++i) if (nums[i] >= 0) total = insert(outside, nums[i], total, k);
      for (int end = n - 1; end >= start; --end) {
        answer = Math.max(answer, prefix[end + 1] - prefix[start] + benefit[end] + total);
        if (nums[end] >= 0) {
          total = insert(outside, nums[end], total, k);
          answer = Math.max(answer, total);
        }
      }
    }
    return answer;
  }
}
