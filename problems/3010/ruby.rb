# @return {Integer}
def minimum_cost(nums)
  first = second = Float::INFINITY
  nums.drop(1).each do |x|
    if x < first
      first, second = x, first
    elsif x < second
      second = x
    end
  end
  nums[0] + first + second
end
