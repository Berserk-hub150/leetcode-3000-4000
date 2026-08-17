class Solution {
public:
    int maxFrequencyElements(vector<int>& nums) {
        unordered_map<int, int> freq;
        int best = 0;
        for (int x : nums) best = max(best, ++freq[x]);
        int ans = 0;
        for (auto& [_, count] : freq) if (count == best) ans += count;
        return ans;
    }
};
