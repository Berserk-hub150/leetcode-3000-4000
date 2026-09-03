// SPDX-License-Identifier: MIT
// Java adaptation; original Copyright (c) 2018 kamyu104/LeetCode-Solutions.
// Source:
// https://github.com/kamyu104/LeetCode-Solutions/blob/6909130180642cdd7010731c73daecaed3cc772c/C%2B%2B/maximum-score-with-co-prime-element.cpp
// Changes and license scope: metadata.json, ../../NOTICE.md and ../../LICENSE_SCOPE.md.

import java.util.*;

// Mobius inversion counts the existing values coprime to each candidate.
// Time: O(n + R*log(R)). Space: O(R), R = max(maxVal, max(nums)).
class Solution {
  public int maxScore(int[] nums, int maxVal) {
    int range = maxVal;
    for (int x : nums) range = Math.max(range, x);
    int[] spf = new int[range + 1], mu = new int[range + 1];
    int[] primes = new int[range + 1];
    int count = 0;
    mu[1] = 1;
    for (int i = 2; i <= range; ++i) {
      if (spf[i] == 0) {
        spf[i] = i;
        primes[count++] = i;
      }
      for (int j = 0; j < count && primes[j] <= spf[i] && (long) i * primes[j] <= range; ++j)
        spf[i * primes[j]] = primes[j];
      mu[i] = spf[i / spf[i]] == spf[i] ? 0 : -mu[i / spf[i]];
    }
    int[] frequency = new int[range + 1], coprime = new int[range + 1];
    for (int x : nums) ++frequency[x];
    for (int i = 1; i <= range; ++i) {
      if (mu[i] == 0) continue;
      int multiples = 0;
      for (int j = i; j <= range; j += i) multiples += frequency[j];
      for (int j = i; j <= range; j += i) coprime[j] += mu[i] * multiples;
    }
    int answer = 0;
    for (int i = 1; i <= range; ++i) {
      int changes = nums.length - coprime[i];
      if (frequency[i] > 0) answer = Math.max(answer, i - (i == 1 ? 0 : changes - 1));
      else if (i <= maxVal) answer = Math.max(answer, i - Math.max(changes, 1));
    }
    return answer;
  }
}
