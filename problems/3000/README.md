# 3000. Maximum Area of Longest Diagonal Rectangle

Official problem: https://leetcode.com/problems/maximum-area-of-longest-diagonal-rectangle/

## Approach

Compare squared diagonal lengths (`length² + width²`) so no floating-point arithmetic is needed. Keep the area of the rectangle with the largest squared diagonal; on a tie, keep the larger area.

- Time: **O(n)**
- Extra space: **O(1)**

The implementations in this directory are original translations of the same algorithm. Racket/Erlang/Elixir are kept `unverified` until their current LeetCode wrapper/signature is checked directly.
