defmodule Solution do
  def min_moves_to_capture_the_queen(a, b, c, d, e, f) do
    between = fn x, y, z -> min(x, z) < y and y < max(x, z) end
    rook_blocked = (a == e and c == a and between.(b, d, f)) or
                   (b == f and d == b and between.(a, c, e))

    cond do
      (a == e or b == f) and not rook_blocked -> 1
      true ->
        bishop_attacks = abs(c - e) == abs(d - f)
        bishop_blocked = bishop_attacks and abs(a - e) == abs(b - f) and
                         between.(c, a, e) and between.(d, b, f)
        if bishop_attacks and not bishop_blocked, do: 1, else: 2
    end
  end
end
