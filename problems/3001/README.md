# 3001. Minimum Moves to Capture The Queen

Official problem: https://leetcode.com/problems/minimum-moves-to-capture-the-queen/

## Approach

The answer is either 1 or 2. Check whether the rook attacks the queen on the same row/column without the bishop lying strictly between them. Then check whether the bishop attacks the queen diagonally without the rook lying strictly between them. If neither can capture immediately, two moves always suffice.

- Time: **O(1)**
- Extra space: **O(1)**
