object Solution {
    def maxFrequencyElements(nums: Array[Int]): Int = {
        val freq = scala.collection.mutable.Map.empty[Int, Int].withDefaultValue(0)
        var best = 0
        for (x <- nums) {
            freq(x) += 1
            best = math.max(best, freq(x))
        }
        freq.values.filter(_ == best).sum
    }
}
