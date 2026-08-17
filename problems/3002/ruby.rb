require 'set'

# @return {Integer}
def maximum_set_size(nums1, nums2)
  s1, s2 = nums1.to_set, nums2.to_set
  half = nums1.length / 2
  [[s1.length, half].min + [s2.length, half].min, (s1 | s2).length].min
end
