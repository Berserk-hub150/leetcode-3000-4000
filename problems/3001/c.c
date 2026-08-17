static int between3001(int x, int y, int z) {
    int lo = x < z ? x : z, hi = x > z ? x : z;
    return lo < y && y < hi;
}

int minMovesToCaptureTheQueen(int a, int b, int c, int d, int e, int f) {
    int rookBlocked = (a == e && c == a && between3001(b, d, f)) ||
                      (b == f && d == b && between3001(a, c, e));
    if ((a == e || b == f) && !rookBlocked) return 1;

    int bishopAttacks = abs(c - e) == abs(d - f);
    int bishopBlocked = bishopAttacks && abs(a - e) == abs(b - f) &&
                        between3001(c, a, e) && between3001(d, b, f);
    return bishopAttacks && !bishopBlocked ? 1 : 2;
}
