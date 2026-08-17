class Solution {
  int minMovesToCaptureTheQueen(int a, int b, int c, int d, int e, int f) {
    bool between(int x, int y, int z) => (x < z ? x : z) < y && y < (x > z ? x : z);
    int abs(int x) => x < 0 ? -x : x;

    final rookBlocked = (a == e && c == a && between(b, d, f)) ||
                        (b == f && d == b && between(a, c, e));
    if ((a == e || b == f) && !rookBlocked) return 1;

    final bishopAttacks = abs(c - e) == abs(d - f);
    final bishopBlocked = bishopAttacks && abs(a - e) == abs(b - f) &&
                          between(c, a, e) && between(d, b, f);
    return bishopAttacks && !bishopBlocked ? 1 : 2;
  }
}
