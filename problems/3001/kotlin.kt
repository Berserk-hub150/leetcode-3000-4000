class Solution {
    fun minMovesToCaptureTheQueen(a: Int, b: Int, c: Int, d: Int, e: Int, f: Int): Int {
        fun between(x: Int, y: Int, z: Int) = minOf(x, z) < y && y < maxOf(x, z)
        val rookBlocked = (a == e && c == a && between(b, d, f)) ||
                          (b == f && d == b && between(a, c, e))
        if ((a == e || b == f) && !rookBlocked) return 1

        val bishopAttacks = kotlin.math.abs(c - e) == kotlin.math.abs(d - f)
        val bishopBlocked = bishopAttacks && kotlin.math.abs(a - e) == kotlin.math.abs(b - f) &&
                            between(c, a, e) && between(d, b, f)
        return if (bishopAttacks && !bishopBlocked) 1 else 2
    }
}
