public class Solution {
    public int MaxFrequencyElements(int[] nums) {
        int[] freq = new int[101];
        int best = 0;
        foreach (int x in nums) best = System.Math.Max(best, ++freq[x]);
        int ans = 0;
        foreach (int count in freq) if (count == best) ans += count;
        return ans;
    }
}
