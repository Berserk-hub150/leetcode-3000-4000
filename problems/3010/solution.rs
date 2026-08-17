impl Solution {
    pub fn minimum_cost(nums: Vec<i32>) -> i32 {
        let (mut first, mut second) = (i32::MAX, i32::MAX);
        for &x in &nums[1..] {
            if x < first { second = first; first = x; }
            else if x < second { second = x; }
        }
        nums[0] + first + second
    }
}
