object Solution {
    def minMovesToCaptureTheQueen(a: Int, b: Int, c: Int, d: Int, e: Int, f: Int): Int = {
        def between(x: Int, y: Int, z: Int): Boolean = math.min(x, z) < y && y < math.max(x, z)
        val rookBlocked = (a == e && c == a && between(b, d, f)) ||
                          (b == f && d == b && between(a, c, e))
        if ((a == e || b == f) && !rookBlocked) return 1

        val bishopAttacks = math.abs(c - e) == math.abs(d - f)
        val bishopBlocked = bishopAttacks && math.abs(a - e) == math.abs(b - f) &&
                            between(c, a, e) && between(d, b, f)
        if (bishopAttacks && !bishopBlocked) 1 else 2
    }
}
