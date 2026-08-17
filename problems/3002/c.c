#include <stdlib.h>

static int cmp3002(const void* a, const void* b) {
    int x = *(const int*)a, y = *(const int*)b;
    return (x > y) - (x < y);
}

static int unique3002(int* a, int n) {
    qsort(a, n, sizeof(int), cmp3002);
    int k = 0;
    for (int i = 0; i < n; ++i)
        if (i == 0 || a[i] != a[i - 1]) a[k++] = a[i];
    return k;
}

int maximumSetSize(int* nums1, int nums1Size, int* nums2, int nums2Size) {
    int n = nums1Size, half = n / 2;
    int u1 = unique3002(nums1, n), u2 = unique3002(nums2, nums2Size);
    int i = 0, j = 0, uni = 0;
    while (i < u1 || j < u2) {
        if (j == u2 || (i < u1 && nums1[i] < nums2[j])) { ++i; ++uni; }
        else if (i == u1 || nums2[j] < nums1[i]) { ++j; ++uni; }
        else { ++i; ++j; ++uni; }
    }
    int cap1 = u1 < half ? u1 : half;
    int cap2 = u2 < half ? u2 : half;
    return uni < cap1 + cap2 ? uni : cap1 + cap2;
}
