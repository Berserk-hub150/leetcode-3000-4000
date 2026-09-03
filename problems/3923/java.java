// SPDX-License-Identifier: MIT
// Java adaptation; original Copyright (c) 2018 kamyu104/LeetCode-Solutions.
// Source:
// https://github.com/kamyu104/LeetCode-Solutions/blob/6909130180642cdd7010731c73daecaed3cc772c/C%2B%2B/minimum-generations-to-target-point.cpp
// Changes and license scope: metadata.json, ../../NOTICE.md and ../../LICENSE_SCOPE.md.

import java.util.*;

class Solution {
  private int encode(int[] p) {
    return p[0] * 49 + p[1] * 7 + p[2];
  }

  public int minGenerations(int[][] points, int[] target) {
    boolean[] seen = new boolean[343];
    List<int[]> all = new ArrayList<>();
    int goal = encode(target);
    for (int[] p : points) {
      int key = encode(p);
      if (key == goal) return 0;
      if (!seen[key]) {
        seen[key] = true;
        all.add(p);
      }
    }
    int end = 0, generation = 0;
    for (int i = 0; i < all.size(); i++) {
      if (i == end) {
        end = all.size();
        generation++;
      }
      for (int j = 0; j < i; j++) {
        int[] a = all.get(i), b = all.get(j);
        int[] next = {(a[0] + b[0]) / 2, (a[1] + b[1]) / 2, (a[2] + b[2]) / 2};
        int key = encode(next);
        if (seen[key]) continue;
        if (key == goal) return generation;
        seen[key] = true;
        all.add(next);
      }
    }
    return -1;
  }
}
