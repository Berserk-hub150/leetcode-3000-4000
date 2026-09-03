// #Medium #Math #Binary_Search #Weekly_Contest_474
// #2026_07_23_Time_1_ms_(100.00%)_Space_43.99_MB_(84.21%)

class Solution {
    private boolean isPossible(long k, long n1, long n2, int p1, int p2, long lVal) {
        long kP1 = k / p1;
        long kP2 = k / p2;
        long kL = k / lVal;
        long s1 = kP2 - kL;
        long s2 = kP1 - kL;
        long sB = k - kP1 - kP2 + kL;
        long w1 = Math.max(0L, n1 - s1);
        long w2 = Math.max(0L, n2 - s2);
        return (w1 + w2) <= sB;
    }

    private long findGcd(long a, long b) {
        long x = a;
        long y = b;
        while (y != 0) {
            long temp = y;
            y = x % y;
            x = temp;
        }
        return x;
    }

    public long minimumTime(int[] d, int[] r) {
        long n1 = d[0];
        long n2 = d[1];
        int p1 = r[0];
        int p2 = r[1];
        long g = findGcd(p1, p2);
        long l = (long) p1 * p2 / g;
        long lo = n1 + n2;
        long hi = (n1 + n2) * Math.max(p1, p2);
        long res = hi;
        while (lo <= hi) {
            long mid = lo + (hi - lo) / 2;
            if (isPossible(mid, n1, n2, p1, p2, l)) {
                res = mid;
                hi = mid - 1;
            } else {
                lo = mid + 1;
            }
        }
        return res;
    }
}
