class Solution:
    def findMaximumNumber(self, k: int, x: int) -> int:
        def accumulated_price(value: int) -> int:
            total = 0
            bit = x - 1
            count = value + 1
            while (1 << bit) <= value:
                half = 1 << bit
                cycle = half << 1
                full, rem = divmod(count, cycle)
                total += full * half + max(0, rem - half)
                bit += x
            return total

        lo, hi = 0, 1
        while accumulated_price(hi) <= k:
            hi <<= 1
        while lo + 1 < hi:
            mid = (lo + hi) // 2
            if accumulated_price(mid) <= k:
                lo = mid
            else:
                hi = mid
        return lo
