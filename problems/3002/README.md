# 3002. Maximum Size of a Set After Removals

Official problem: https://leetcode.com/problems/maximum-size-of-a-set-after-removals/

## Approach

Let `S1` and `S2` be the distinct values in each array. After removing half of each array, each side can keep at most `n/2` distinct values. Therefore the answer is the smaller of:

1. `min(|S1|, n/2) + min(|S2|, n/2)`, and
2. `|S1 ∪ S2|`.

- Time: **O(n)** expected with hash sets
- Extra space: **O(n)**
