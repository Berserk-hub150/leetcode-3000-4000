type fenwick []int64

func (f fenwick) update(i int, val int64) {
	for ; i < len(f); i += i & -i {
		f[i] = max(f[i], val)
	}
}

func (f fenwick) preMax(i int) (res int64) {
	for ; i > 0; i &= i - 1 {
		res = max(res, f[i])
	}
	return
}

func maxAlternatingSum(nums []int, k int) (ans int64) {
	sorted := slices.Clone(nums)
	slices.Sort(sorted)
	sorted = slices.Compact(sorted)

	n := len(nums)
	fInc := make([]int64, n)
	fDec := make([]int64, n)

	m := len(sorted)
	inc := make(fenwick, m+1)
	dec := make(fenwick, m+1)

	for i, x := range nums {
		if i >= k {
			j := nums[i-k]
			inc.update(m-j, fInc[i-k])
			dec.update(j+1, fDec[i-k])
		}

		j := sort.SearchInts(sorted, x)
		nums[i] = j

		fInc[i] = dec.preMax(j) + int64(x)
		fDec[i] = inc.preMax(m-1-j) + int64(x)
		ans = max(ans, fInc[i], fDec[i])
	}

	return
}
