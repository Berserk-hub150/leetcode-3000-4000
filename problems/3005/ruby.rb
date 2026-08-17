# @param {Integer[]} nums
# @return {Integer}
def max_frequency_elements(nums)
  freq = Hash.new(0)
  nums.each { |x| freq[x] += 1 }
  best = freq.values.max
  freq.values.select { |count| count == best }.sum
end
