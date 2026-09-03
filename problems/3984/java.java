// SPDX-License-Identifier: MIT
// Java adaptation; original Copyright (c) 2018 kamyu104/LeetCode-Solutions.
// Source:
// https://github.com/kamyu104/LeetCode-Solutions/blob/6909130180642cdd7010731c73daecaed3cc772c/C%2B%2B/divisible-game.cpp
// Changes and license scope: metadata.json, ../../NOTICE.md and ../../LICENSE_SCOPE.md.

import java.util.*;

// Group positions by prime factor, then apply weighted Kadane to each group.
// Time: O(R*log(log(R)) + n*log(R)). Space: O(R+n*log(R)).
class Solution {
  public int divisibleGame(int[] nums) {
    final long mod = 1_000_000_007L;
    int range = 1, smallest = Integer.MAX_VALUE;
    for (int x : nums) {
      range = Math.max(range, x);
      smallest = Math.min(smallest, x);
    }
    int[] spf = new int[range + 1];
    for (int p = 2; p <= range; ++p)
      if (spf[p] == 0) {
        spf[p] = p;
        if ((long) p * p <= range)
          for (int multiple = p * p; multiple <= range; multiple += p)
            if (spf[multiple] == 0) spf[multiple] = p;
      }
    long[] prefix = new long[nums.length + 1];
    Map<Integer, List<Integer>> positions = new HashMap<>();
    for (int i = 0; i < nums.length; ++i) {
      prefix[i + 1] = prefix[i] + nums[i];
      int x = nums[i];
      while (x > 1) {
        int prime = spf[x];
        positions.computeIfAbsent(prime, unused -> new ArrayList<>()).add(i);
        while (x % prime == 0) x /= prime;
      }
    }
    long bestDifference = -smallest;
    int bestPrime = 2;
    for (Map.Entry<Integer, List<Integer>> entry : positions.entrySet()) {
      int prime = entry.getKey(), previous = -1;
      long total = 0;
      for (int i : entry.getValue()) {
        total = Math.max(total - (prefix[i] - prefix[previous + 1]), 0) + nums[i];
        if (total > bestDifference || total == bestDifference && prime < bestPrime) {
          bestDifference = total;
          bestPrime = prime;
        }
        previous = i;
      }
    }
    return (int) ((bestDifference % mod * bestPrime % mod + mod) % mod);
  }
}
