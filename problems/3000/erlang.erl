-spec area_of_max_diagonal([[integer()]]) -> integer().
area_of_max_diagonal(Dimensions) ->
    {_BestDiag, BestArea} = lists:foldl(
        fun([Length, Width], {BD, BA}) ->
            Diag = Length * Length + Width * Width,
            Area = Length * Width,
            case (Diag > BD) orelse ((Diag =:= BD) andalso (Area > BA)) of
                true -> {Diag, Area};
                false -> {BD, BA}
            end
        end,
        {0, 0},
        Dimensions
    ),
    BestArea.
