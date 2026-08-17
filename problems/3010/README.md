# 3010. Divide an Array Into Subarrays With Minimum Cost I

Official problem: https://leetcode.com/problems/divide-an-array-into-subarrays-with-minimum-cost-i/

## Approach

The first subarray always starts at index 0. The other two subarrays can start at any two later indices, so minimize the total by choosing the two smallest values in `nums[1:]`.

- Time: **O(n)**
- Extra space: **O(1)**
