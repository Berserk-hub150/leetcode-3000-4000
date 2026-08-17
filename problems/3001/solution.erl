-spec min_moves_to_capture_the_queen(integer(), integer(), integer(), integer(), integer(), integer()) -> integer().
min_moves_to_capture_the_queen(A, B, C, D, E, F) ->
    Between = fun(X, Y, Z) -> erlang:min(X, Z) < Y andalso Y < erlang:max(X, Z) end,
    RookBlocked = (A =:= E andalso C =:= A andalso Between(B, D, F)) orelse
                  (B =:= F andalso D =:= B andalso Between(A, C, E)),
    case (A =:= E orelse B =:= F) andalso not RookBlocked of
        true -> 1;
        false ->
            BishopAttacks = abs(C - E) =:= abs(D - F),
            BishopBlocked = BishopAttacks andalso abs(A - E) =:= abs(B - F) andalso
                            Between(C, A, E) andalso Between(D, B, F),
            case BishopAttacks andalso not BishopBlocked of true -> 1; false -> 2 end
    end.
