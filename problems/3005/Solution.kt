class Solution {
    fun maxFrequencyElements(nums: IntArray): Int {
        val freq = IntArray(101)
        var best = 0
        for (x in nums) {
            freq[x]++
            best = maxOf(best, freq[x])
        }
        return freq.filter { it == best }.sum()
    }
}
