// SPDX-License-Identifier: MIT
// Java adaptation; original Copyright (c) 2018 kamyu104/LeetCode-Solutions.
// Source:
// https://github.com/kamyu104/LeetCode-Solutions/blob/6909130180642cdd7010731c73daecaed3cc772c/C%2B%2B/good-subsequence-queries.cpp
// Changes and license scope: metadata.json, ../../NOTICE.md and ../../LICENSE_SCOPE.md.

class Solution {
  private int gcd(int a, int b) {
    while (b != 0) {
      int t = a % b;
      a = b;
      b = t;
    }
    return a;
  }

  public int countGoodSubseq(int[] nums, int p, int[][] queries) {
    if (nums.length == 1) return 0;
    int n = nums.length, size = 1;
    while (size < n) size <<= 1;
    int[] tree = new int[size * 2], values = nums.clone();
    int divisible = 0;
    for (int i = 0; i < n; i++)
      if (values[i] % p == 0) {
        tree[size + i] = values[i] / p;
        divisible++;
      }
    for (int i = size - 1; i > 0; i--) tree[i] = gcd(tree[i * 2], tree[i * 2 + 1]);
    int answer = 0;
    for (int[] query : queries) {
      int index = query[0], x = query[1];
      if (values[index] % p == 0) divisible--;
      values[index] = x;
      if (x % p == 0) divisible++;
      int pos = size + index;
      tree[pos] = x % p == 0 ? x / p : 0;
      for (pos >>= 1; pos > 0; pos >>= 1) tree[pos] = gcd(tree[pos * 2], tree[pos * 2 + 1]);
      if (divisible == 0 || tree[1] != 1) continue;
      // Values are at most 50,000: a minimal gcd-one witness has at most
      // six elements. For larger arrays that witness is a proper subset.
      if (divisible < n || n > 6) {
        answer++;
        continue;
      }
      for (int omit = 0; omit < n; omit++) {
        int g = 0;
        for (int i = 0; i < n; i++) if (i != omit) g = gcd(g, values[i] / p);
        if (g == 1) {
          answer++;
          break;
        }
      }
    }
    return answer;
  }
}
