# @return {Integer}
def min_moves_to_capture_the_queen(a, b, c, d, e, f)
  between = ->(x, y, z) { [x, z].min < y && y < [x, z].max }
  rook_blocked = (a == e && c == a && between.call(b, d, f)) ||
                 (b == f && d == b && between.call(a, c, e))
  return 1 if (a == e || b == f) && !rook_blocked

  bishop_attacks = (c - e).abs == (d - f).abs
  bishop_blocked = bishop_attacks && (a - e).abs == (b - f).abs &&
                   between.call(c, a, e) && between.call(d, b, f)
  bishop_attacks && !bishop_blocked ? 1 : 2
end
