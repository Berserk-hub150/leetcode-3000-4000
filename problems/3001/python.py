class Solution:
    def minMovesToCaptureTheQueen(self, a: int, b: int, c: int, d: int, e: int, f: int) -> int:
        between = lambda x, y, z: min(x, z) < y < max(x, z)

        rook_blocked = (a == e and c == a and between(b, d, f)) or (b == f and d == b and between(a, c, e))
        if (a == e or b == f) and not rook_blocked:
            return 1

        bishop_attacks = abs(c - e) == abs(d - f)
        bishop_blocked = bishop_attacks and abs(a - e) == abs(b - f) and between(c, a, e) and between(d, b, f)
        if bishop_attacks and not bishop_blocked:
            return 1
        return 2
