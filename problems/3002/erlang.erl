-spec maximum_set_size([integer()], [integer()]) -> integer().
maximum_set_size(Nums1, Nums2) ->
    S1 = sets:from_list(Nums1),
    S2 = sets:from_list(Nums2),
    Half = length(Nums1) div 2,
    min(sets:size(sets:union(S1, S2)), min(sets:size(S1), Half) + min(sets:size(S2), Half)).
