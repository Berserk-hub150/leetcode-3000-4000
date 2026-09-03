// #Medium #Array #Dynamic_Programming #Math #2025_04_22_Time_12_ms_(95.54%)_Space_61.08_MB_(18.22%)

class Solution {
    public long[] resultArray(int[] nums, int k) {
        long[] res = new long[k];
        int[] cnt = new int[k];
        for (int a : nums) {
            int[] cnt2 = new int[k];
            for (int i = 0; i < k; i++) {
                int v = (int) (((long) i * a) % k);
                cnt2[v] += cnt[i];
                res[v] += cnt[i];
            }
            cnt = cnt2;
            cnt[a % k]++;
            res[a % k]++;
        }
        return res;
    }
}
