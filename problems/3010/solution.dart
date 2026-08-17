class Solution {
  int minimumCost(List<int> nums) {
    var first = 1 << 60, second = 1 << 60;
    for (var i = 1; i < nums.length; ++i) {
      final x = nums[i];
      if (x < first) { second = first; first = x; }
      else if (x < second) second = x;
    }
    return nums[0] + first + second;
  }
}
