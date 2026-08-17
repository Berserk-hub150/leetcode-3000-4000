object Solution {
    def minimumCost(nums: Array[Int]): Int = {
        var first = Int.MaxValue
        var second = Int.MaxValue
        for (i <- 1 until nums.length) {
            val x = nums(i)
            if (x < first) { second = first; first = x }
            else if (x < second) second = x
        }
        nums(0) + first + second
    }
}
