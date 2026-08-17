impl Solution {
    pub fn min_moves_to_capture_the_queen(a: i32, b: i32, c: i32, d: i32, e: i32, f: i32) -> i32 {
        let between = |x: i32, y: i32, z: i32| x.min(z) < y && y < x.max(z);
        let rook_blocked = (a == e && c == a && between(b, d, f)) ||
                           (b == f && d == b && between(a, c, e));
        if (a == e || b == f) && !rook_blocked { return 1; }

        let bishop_attacks = (c - e).abs() == (d - f).abs();
        let bishop_blocked = bishop_attacks && (a - e).abs() == (b - f).abs() &&
                             between(c, a, e) && between(d, b, f);
        if bishop_attacks && !bishop_blocked { 1 } else { 2 }
    }
}
