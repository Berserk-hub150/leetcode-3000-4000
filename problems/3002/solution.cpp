class Solution {
public:
    int maximumSetSize(vector<int>& nums1, vector<int>& nums2) {
        unordered_set<int> s1(nums1.begin(), nums1.end());
        unordered_set<int> s2(nums2.begin(), nums2.end());
        unordered_set<int> all = s1;
        all.insert(s2.begin(), s2.end());
        int half = nums1.size() / 2;
        return min((int)all.size(), min((int)s1.size(), half) + min((int)s2.size(), half));
    }
};
