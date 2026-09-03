// SPDX-License-Identifier: MIT
// Java adaptation; original Copyright (c) 2018 kamyu104/LeetCode-Solutions.
// Source:
// https://github.com/kamyu104/LeetCode-Solutions/blob/6909130180642cdd7010731c73daecaed3cc772c/C%2B%2B/maximum-sum-of-m-non-overlapping-subarrays-i.cpp
// Changes and license scope: metadata.json, ../../NOTICE.md and ../../LICENSE_SCOPE.md.

// Penalized DP and a monotone queue (ties prefer fewer segments).
// Time: O(n*log(S)). Space: O(n), S = maximum positive subarray sum.
class Solution {
  private long[] prefix;
  private int lower, upper;

  private boolean better(long value, int count, long other, int otherCount) {
    return value > other || value == other && count < otherCount;
  }

  private long[] evaluate(long penalty) {
    int n = prefix.length - 1;
    long[] dp = new long[n + 1];
    int[] count = new int[n + 1], queue = new int[n + 1];
    int head = 0, tail = 0;
    for (int i = 1; i <= n; ++i) {
      int j = i - lower;
      if (j >= 0) {
        while (head < tail
            && better(
                dp[j] - prefix[j],
                count[j],
                dp[queue[tail - 1]] - prefix[queue[tail - 1]],
                count[queue[tail - 1]])) --tail;
        queue[tail++] = j;
      }
      while (head < tail && queue[head] < i - upper) ++head;
      dp[i] = dp[i - 1];
      count[i] = count[i - 1];
      if (head < tail) {
        j = queue[head];
        long candidate = dp[j] - prefix[j] + prefix[i] - penalty;
        if (better(candidate, count[j] + 1, dp[i], count[i])) {
          dp[i] = candidate;
          count[i] = count[j] + 1;
        }
      }
    }
    return new long[] {dp[n], count[n]};
  }

  public long maximumSum(int[] nums, int m, int l, int r) {
    int n = nums.length;
    lower = l;
    upper = r;
    prefix = new long[n + 1];
    for (int i = 0; i < n; ++i) prefix[i + 1] = prefix[i] + nums[i];
    int[] queue = new int[n + 1];
    int head = 0, tail = 0;
    long bestSingle = Long.MIN_VALUE;
    for (int i = l; i <= n; ++i) {
      int j = i - l;
      while (head < tail && prefix[queue[tail - 1]] >= prefix[j]) --tail;
      queue[tail++] = j;
      while (queue[head] < i - r) ++head;
      bestSingle = Math.max(bestSingle, prefix[i] - prefix[queue[head]]);
    }
    long[] result = evaluate(0);
    if (result[1] == 0) return bestSingle;
    if (result[1] <= m) return result[0];
    long low = 1, high = bestSingle;
    while (low < high) {
      long middle = low + (high - low) / 2;
      if (evaluate(middle)[1] <= m) high = middle;
      else low = middle + 1;
    }
    return evaluate(low)[0] + m * low;
  }
}
