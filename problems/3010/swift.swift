class Solution {
    func minimumCost(_ nums: [Int]) -> Int {
        var first = Int.max, second = Int.max
        for x in nums.dropFirst() {
            if x < first { second = first; first = x }
            else if x < second { second = x }
        }
        return nums[0] + first + second
    }
}
