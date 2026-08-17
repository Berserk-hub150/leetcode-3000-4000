impl Solution {
    pub fn max_frequency_elements(nums: Vec<i32>) -> i32 {
        let mut freq = [0i32; 101];
        let mut best = 0;
        for x in nums {
            freq[x as usize] += 1;
            best = best.max(freq[x as usize]);
        }
        freq.into_iter().filter(|&c| c == best).sum()
    }
}
