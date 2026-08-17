function minimumCost(nums: number[]): number {
    let first = Infinity, second = Infinity;
    for (let i = 1; i < nums.length; ++i) {
        const x = nums[i];
        if (x < first) { second = first; first = x; }
        else if (x < second) second = x;
    }
    return nums[0] + first + second;
}
