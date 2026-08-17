-spec max_frequency_elements([integer()]) -> integer().
max_frequency_elements(Nums) ->
    Freq = lists:foldl(fun(X, M) -> maps:update_with(X, fun(V) -> V + 1 end, 1, M) end, #{}, Nums),
    Values = maps:values(Freq),
    Best = lists:max(Values),
    lists:sum([V || V <- Values, V =:= Best]).
