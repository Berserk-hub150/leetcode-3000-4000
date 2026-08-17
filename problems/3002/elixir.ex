defmodule Solution do
  def maximum_set_size(nums1, nums2) do
    s1 = MapSet.new(nums1)
    s2 = MapSet.new(nums2)
    half = div(length(nums1), 2)
    min(MapSet.size(MapSet.union(s1, s2)), min(MapSet.size(s1), half) + min(MapSet.size(s2), half))
  end
end
