public class Solution {
    public int MinimumCost(int[] nums) {
        int first = int.MaxValue, second = int.MaxValue;
        for (int i = 1; i < nums.Length; ++i) {
            int x = nums[i];
            if (x < first) { second = first; first = x; }
            else if (x < second) second = x;
        }
        return nums[0] + first + second;
    }
}
