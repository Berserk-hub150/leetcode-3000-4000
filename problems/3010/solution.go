func minimumCost(nums []int) int {
    const inf = int(^uint(0) >> 1)
    first, second := inf, inf
    for _, x := range nums[1:] {
        if x < first { second, first = first, x } else if x < second { second = x }
    }
    return nums[0] + first + second
}
