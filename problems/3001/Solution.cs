public class Solution {
    private bool Between(int x, int y, int z) => System.Math.Min(x, z) < y && y < System.Math.Max(x, z);

    public int MinMovesToCaptureTheQueen(int a, int b, int c, int d, int e, int f) {
        bool rookBlocked = (a == e && c == a && Between(b, d, f)) ||
                           (b == f && d == b && Between(a, c, e));
        if ((a == e || b == f) && !rookBlocked) return 1;

        bool bishopAttacks = System.Math.Abs(c - e) == System.Math.Abs(d - f);
        bool bishopBlocked = bishopAttacks && System.Math.Abs(a - e) == System.Math.Abs(b - f) &&
                             Between(c, a, e) && Between(d, b, f);
        return bishopAttacks && !bishopBlocked ? 1 : 2;
    }
}
