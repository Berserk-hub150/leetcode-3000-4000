class Solution {
    fun minimumCost(nums: IntArray): Int {
        var first = Int.MAX_VALUE
        var second = Int.MAX_VALUE
        for (i in 1 until nums.size) {
            val x = nums[i]
            if (x < first) { second = first; first = x }
            else if (x < second) second = x
        }
        return nums[0] + first + second
    }
}
