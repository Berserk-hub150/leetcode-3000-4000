func maxFrequencyElements(nums []int) int {
    freq := make(map[int]int)
    best := 0
    for _, x := range nums {
        freq[x]++
        if freq[x] > best { best = freq[x] }
    }
    ans := 0
    for _, count := range freq {
        if count == best { ans += count }
    }
    return ans
}
