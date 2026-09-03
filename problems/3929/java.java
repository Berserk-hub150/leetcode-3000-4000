// SPDX-License-Identifier: MIT
// Java adaptation; original Copyright (c) 2018 kamyu104/LeetCode-Solutions.
// Source:
// https://github.com/kamyu104/LeetCode-Solutions/blob/6909130180642cdd7010731c73daecaed3cc772c/C%2B%2B/minimum-partition-score-ii.cpp
// Changes and license scope: metadata.json, ../../NOTICE.md and ../../LICENSE_SCOPE.md.

import java.math.*;
import java.util.*;

class Solution {
  private record Line(long slope, long intercept, int groups) {
    long value(long x) {
      return slope * x + intercept;
    }
  }

  private boolean keep(Line a, Line b, Line c) {
    BigInteger left =
        BigInteger.valueOf(b.intercept - a.intercept)
            .multiply(BigInteger.valueOf(b.slope - c.slope));
    BigInteger right =
        BigInteger.valueOf(c.intercept - b.intercept)
            .multiply(BigInteger.valueOf(a.slope - b.slope));
    return left.compareTo(right) < 0;
  }

  private long[] evaluate(long[] prefix, long penalty) {
    Deque<Line> hull = new ArrayDeque<>();
    hull.add(new Line(0, 0, 0));
    long dp = 0;
    int groups = 0;
    for (int i = 1; i < prefix.length; i++) {
      long x = prefix[i];
      while (hull.size() >= 2) {
        Line first = hull.removeFirst(), second = hull.peekFirst();
        if (first.value(x) <= second.value(x)) {
          hull.addFirst(first);
          break;
        }
      }
      Line best = hull.peekFirst();
      dp = best.value(x) + x * (x + 1) / 2 + penalty;
      groups = best.groups + 1;
      Line line = new Line(-x, dp + x * (x - 1) / 2, groups);
      while (hull.size() >= 2) {
        Line last = hull.removeLast(), before = hull.peekLast();
        if (keep(before, last, line)) {
          hull.addLast(last);
          break;
        }
      }
      hull.addLast(line);
    }
    return new long[] {dp, groups};
  }

  public long minPartitionScore(int[] nums, int k) {
    long[] prefix = new long[nums.length + 1];
    for (int i = 0; i < nums.length; i++) prefix[i + 1] = prefix[i] + nums[i];
    long total = prefix[nums.length] * (prefix[nums.length] + 1) / 2, high = 0;
    for (int i = 1; i < nums.length; i++)
      high =
          Math.max(
              high,
              total
                  - prefix[i] * (prefix[i] + 1) / 2
                  - (prefix[nums.length] - prefix[i]) * (prefix[nums.length] - prefix[i] + 1) / 2);
    long lo = 0;
    while (lo < high) {
      long mid = lo + (high - lo) / 2;
      if (evaluate(prefix, mid)[1] <= k) high = mid;
      else lo = mid + 1;
    }
    return evaluate(prefix, lo)[0] - lo * k;
  }
}
