// SPDX-License-Identifier: CC-BY-SA-4.0
// Java adaptation; original source: doocs/leetcode (CC BY-SA 4.0).
// Source:
// https://github.com/doocs/leetcode/blob/a5ad632a96e9e599012f1d9360fd462e277ea83c/solution/3900-3999/3930.Power%20Update%20After%20K-th%20Largest%20Insertion%20II/README_EN.md
// Changes and license scope: metadata.json, ../../NOTICE.md and ../../LICENSE_SCOPE.md.

import java.util.*;

class Solution {
  private static class Node {
    int key, count = 1, size = 1, priority;
    Node left, right;

    Node(int k, int p) {
      key = k;
      priority = p;
    }
  }

  private int size(Node n) {
    return n == null ? 0 : n.size;
  }

  private void pull(Node n) {
    n.size = n.count + size(n.left) + size(n.right);
  }

  private Node insert(Node n, int key, int priority) {
    if (n == null) return new Node(key, priority);
    if (key == n.key) n.count++;
    else if (key < n.key) {
      n.left = insert(n.left, key, priority);
      if (n.left.priority > n.priority) n = rotateRight(n);
    } else {
      n.right = insert(n.right, key, priority);
      if (n.right.priority > n.priority) n = rotateLeft(n);
    }
    pull(n);
    return n;
  }

  private Node rotateRight(Node n) {
    Node x = n.left;
    n.left = x.right;
    x.right = n;
    pull(n);
    pull(x);
    return x;
  }

  private Node rotateLeft(Node n) {
    Node x = n.right;
    n.right = x.left;
    x.left = n;
    pull(n);
    pull(x);
    return x;
  }

  private int kth(Node n, int k) {
    int left = size(n.left);
    if (k <= left) return kth(n.left, k);
    if (k <= left + n.count) return n.key;
    return kth(n.right, k - left - n.count);
  }

  private long power(long base, int exponent) {
    long answer = 1;
    for (base %= 1_000_000_007L; exponent > 0; exponent >>= 1, base = base * base % 1_000_000_007L)
      if ((exponent & 1) != 0) answer = answer * base % 1_000_000_007L;
    return answer;
  }

  public int[] powerUpdate(int[] nums, int p, int[][] queries) {
    SplittableRandom random = new SplittableRandom(3930);
    Node root = null;
    for (int x : nums) root = insert(root, x, random.nextInt());
    int[] answer = new int[queries.length];
    for (int i = 0; i < queries.length; i++) {
      root = insert(root, queries[i][0], random.nextInt());
      int value = kth(root, size(root) - queries[i][1] + 1);
      p = (int) power(p, value);
      answer[i] = p;
    }
    return answer;
  }
}
