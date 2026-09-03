// #Medium #Array #Stack #Monotonic_Stack #Weekly_Contest_466
// #2025_09_26_Time_2_ms_(100.00%)_Space_58.70_MB_(69.49%)

class Solution {
    public long bowlSubarrays(int[] nums) {
        int n = nums.length;
        int res = n;
        int pre = 0;
        for (int a : nums) {
            if (a > pre) {
                res--;
                pre = a;
            }
        }
        pre = 0;
        for (int i = n - 1; i >= 0; i--) {
            if (nums[i] > pre) {
                res--;
                pre = nums[i];
            }
        }
        return res + 1L;
    }
}
