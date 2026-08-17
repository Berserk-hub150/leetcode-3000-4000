class Solution {
    func minMovesToCaptureTheQueen(_ a: Int, _ b: Int, _ c: Int, _ d: Int, _ e: Int, _ f: Int) -> Int {
        func between(_ x: Int, _ y: Int, _ z: Int) -> Bool { min(x, z) < y && y < max(x, z) }
        let rookBlocked = (a == e && c == a && between(b, d, f)) ||
                          (b == f && d == b && between(a, c, e))
        if (a == e || b == f) && !rookBlocked { return 1 }

        let bishopAttacks = abs(c - e) == abs(d - f)
        let bishopBlocked = bishopAttacks && abs(a - e) == abs(b - f) &&
                            between(c, a, e) && between(d, b, f)
        return bishopAttacks && !bishopBlocked ? 1 : 2
    }
}
