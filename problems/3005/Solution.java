class Solution {
    public int maxFrequencyElements(int[] nums) {
        int[] freq = new int[101];
        int best = 0;
        for (int x : nums) best = Math.max(best, ++freq[x]);
        int ans = 0;
        for (int count : freq) if (count == best) ans += count;
        return ans;
    }
}
