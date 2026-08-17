-spec minimum_cost([integer()]) -> integer().
minimum_cost([Head | Tail]) ->
    [A, B | _] = lists:sort(Tail),
    Head + A + B.
