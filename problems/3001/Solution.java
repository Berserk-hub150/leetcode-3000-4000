class Solution {
    private boolean between(int x, int y, int z) {
        return Math.min(x, z) < y && y < Math.max(x, z);
    }

    public int minMovesToCaptureTheQueen(int a, int b, int c, int d, int e, int f) {
        boolean rookBlocked = (a == e && c == a && between(b, d, f)) ||
                              (b == f && d == b && between(a, c, e));
        if ((a == e || b == f) && !rookBlocked) return 1;

        boolean bishopAttacks = Math.abs(c - e) == Math.abs(d - f);
        boolean bishopBlocked = bishopAttacks && Math.abs(a - e) == Math.abs(b - f) &&
                                between(c, a, e) && between(d, b, f);
        return bishopAttacks && !bishopBlocked ? 1 : 2;
    }
}
