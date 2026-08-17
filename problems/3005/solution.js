/**
 * @param {number[]} nums
 * @return {number}
 */
var maxFrequencyElements = function(nums) {
    const freq = new Map();
    let best = 0;
    for (const x of nums) {
        const count = (freq.get(x) || 0) + 1;
        freq.set(x, count);
        best = Math.max(best, count);
    }
    let ans = 0;
    for (const count of freq.values()) if (count === best) ans += count;
    return ans;
};
