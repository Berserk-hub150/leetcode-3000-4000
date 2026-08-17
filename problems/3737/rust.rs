impl Solution {
    pub fn count_majority_subarrays(nums: Vec<i32>, target: i32) -> i32 {
        let n = nums.len();
        let mut ans = 0;

        for i in 0..n {
            let mut cnt = 0;
            for j in i..n {
                let k = (j - i + 1) as i32;
                if nums[j] == target {
                    cnt += 1;
                }
                if cnt * 2 > k {
                    ans += 1;
                }
            }
        }

        ans
    }
}
