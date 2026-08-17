int maxFrequencyElements(int* nums, int numsSize) {
    int freq[101] = {0};
    int best = 0;
    for (int i = 0; i < numsSize; ++i) {
        int count = ++freq[nums[i]];
        if (count > best) best = count;
    }
    int ans = 0;
    for (int x = 1; x <= 100; ++x)
        if (freq[x] == best) ans += freq[x];
    return ans;
}
