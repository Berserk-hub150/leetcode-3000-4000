class Solution {
    public int minimumCost(int[] nums) {
        int first = Integer.MAX_VALUE, second = Integer.MAX_VALUE;
        for (int i = 1; i < nums.length; ++i) {
            int x = nums[i];
            if (x < first) { second = first; first = x; }
            else if (x < second) second = x;
        }
        return nums[0] + first + second;
    }
}
