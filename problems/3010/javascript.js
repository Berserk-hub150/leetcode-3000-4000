/** @return {number} */
var minimumCost = function(nums) {
    let first = Infinity, second = Infinity;
    for (let i = 1; i < nums.length; ++i) {
        const x = nums[i];
        if (x < first) [first, second] = [x, first];
        else if (x < second) second = x;
    }
    return nums[0] + first + second;
};
