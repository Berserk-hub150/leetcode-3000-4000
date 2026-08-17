class Solution {
    func maxFrequencyElements(_ nums: [Int]) -> Int {
        var freq: [Int: Int] = [:]
        var best = 0
        for x in nums {
            freq[x, default: 0] += 1
            best = max(best, freq[x]!)
        }
        return freq.values.filter { $0 == best }.reduce(0, +)
    }
}
