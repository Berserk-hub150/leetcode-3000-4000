class Solution:
    def minimumTimeToInitialState(self, word: str, k: int) -> int:
        n = len(word)
        z = [0] * n
        left = right = 0
        for i in range(1, n):
            if i <= right:
                z[i] = min(right - i + 1, z[i - left])
            while i + z[i] < n and word[z[i]] == word[i + z[i]]:
                z[i] += 1
            if i + z[i] - 1 > right:
                left, right = i, i + z[i] - 1

        time = 1
        while time * k < n:
            shift = time * k
            if z[shift] >= n - shift:
                return time
            time += 1
        return time
