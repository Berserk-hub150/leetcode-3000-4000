/** @return {number} */
var maximumSetSize = function(nums1, nums2) {
    const s1 = new Set(nums1), s2 = new Set(nums2);
    const all = new Set([...s1, ...s2]);
    const half = nums1.length / 2;
    return Math.min(all.size, Math.min(s1.size, half) + Math.min(s2.size, half));
};
