// #Hard #Math #Recursion #Senior_Staff #Biweekly_Contest_172
// #2026_05_06_Time_1_ms_(100.00%)_Space_43.05_MB_(9.38%)

class Solution {
    public long lastInteger(long n) {
        final long mask = 0xAAAAAAAAAAAAAAAL;
        return ((n - 1) & mask) + 1;
    }
}
