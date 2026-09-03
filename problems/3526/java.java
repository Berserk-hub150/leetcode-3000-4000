// SPDX-License-Identifier: MIT
// Java adaptation; original Copyright (c) 2018 kamyu104/LeetCode-Solutions.
// Source:
// https://github.com/kamyu104/LeetCode-Solutions/blob/6909130180642cdd7010731c73daecaed3cc772c/C%2B%2B/range-xor-queries-with-subarray-reversals.cpp
// Changes and license scope: metadata.json, ../../NOTICE.md and ../../LICENSE_SCOPE.md.

import java.util.*;

// Implicit treap: expected O((n + q) log n) time, O(n) space.
class Solution {
  private static class Node {
    int value, xor, size = 1, priority;
    boolean reversed;
    Node left, right;

    Node(int value, int priority) {
      this.value = this.xor = value;
      this.priority = priority;
    }
  }

  private int size(Node n) {
    return n == null ? 0 : n.size;
  }

  private int xor(Node n) {
    return n == null ? 0 : n.xor;
  }

  private void pull(Node n) {
    if (n != null) {
      n.size = 1 + size(n.left) + size(n.right);
      n.xor = n.value ^ xor(n.left) ^ xor(n.right);
    }
  }

  private void push(Node n) {
    if (n == null || !n.reversed) return;
    Node t = n.left;
    n.left = n.right;
    n.right = t;
    if (n.left != null) n.left.reversed ^= true;
    if (n.right != null) n.right.reversed ^= true;
    n.reversed = false;
  }

  private Node merge(Node a, Node b) {
    if (a == null) return b;
    if (b == null) return a;
    push(a);
    push(b);
    if (a.priority > b.priority) {
      a.right = merge(a.right, b);
      pull(a);
      return a;
    }
    b.left = merge(a, b.left);
    pull(b);
    return b;
  }

  private Node[] split(Node root, int count) {
    if (root == null) return new Node[] {null, null};
    push(root);
    if (size(root.left) >= count) {
      Node[] p = split(root.left, count);
      root.left = p[1];
      pull(root);
      p[1] = root;
      return p;
    }
    Node[] p = split(root.right, count - size(root.left) - 1);
    root.right = p[0];
    pull(root);
    p[0] = root;
    return p;
  }

  public int[] getResults(int[] nums, int[][] queries) {
    SplittableRandom random = new SplittableRandom(3526);
    Node root = null;
    for (int x : nums) root = merge(root, new Node(x, random.nextInt()));
    int[] answers = new int[queries.length];
    int count = 0;
    for (int[] q : queries) {
      Node[] a = split(root, q[1]);
      Node[] b = split(a[1], q[0] == 1 ? 1 : q[2] - q[1] + 1);
      if (q[0] == 1) {
        b[0].value = q[2];
        pull(b[0]);
      } else if (q[0] == 2) answers[count++] = xor(b[0]);
      else b[0].reversed ^= true;
      root = merge(a[0], merge(b[0], b[1]));
    }
    return Arrays.copyOf(answers, count);
  }
}
