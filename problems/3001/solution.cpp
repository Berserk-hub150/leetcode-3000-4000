class Solution {
    bool between(int x, int y, int z) { return min(x, z) < y && y < max(x, z); }
public:
    int minMovesToCaptureTheQueen(int a, int b, int c, int d, int e, int f) {
        bool rookBlocked = (a == e && c == a && between(b, d, f)) ||
                           (b == f && d == b && between(a, c, e));
        if ((a == e || b == f) && !rookBlocked) return 1;

        bool bishopAttacks = abs(c - e) == abs(d - f);
        bool bishopBlocked = bishopAttacks && abs(a - e) == abs(b - f) &&
                             between(c, a, e) && between(d, b, f);
        return bishopAttacks && !bishopBlocked ? 1 : 2;
    }
};
