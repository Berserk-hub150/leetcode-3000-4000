func minMovesToCaptureTheQueen(a int, b int, c int, d int, e int, f int) int {
    between := func(x, y, z int) bool {
        if x > z { x, z = z, x }
        return x < y && y < z
    }
    abs := func(x int) int { if x < 0 { return -x }; return x }

    rookBlocked := (a == e && c == a && between(b, d, f)) ||
        (b == f && d == b && between(a, c, e))
    if (a == e || b == f) && !rookBlocked { return 1 }

    bishopAttacks := abs(c-e) == abs(d-f)
    bishopBlocked := bishopAttacks && abs(a-e) == abs(b-f) &&
        between(c, a, e) && between(d, b, f)
    if bishopAttacks && !bishopBlocked { return 1 }
    return 2
}
