from collections import Counter
import heapq


class Solution:
    def minimizeStringValue(self, s: str) -> str:
        counts = Counter(ch for ch in s if ch != '?')
        heap = [(counts.get(chr(97 + i), 0), chr(97 + i)) for i in range(26)]
        heapq.heapify(heap)
        replacements = []
        for _ in range(s.count('?')):
            count, ch = heapq.heappop(heap)
            replacements.append(ch)
            heapq.heappush(heap, (count + 1, ch))
        replacements.sort()
        chars = list(s)
        it = iter(replacements)
        for i, ch in enumerate(chars):
            if ch == '?':
                chars[i] = next(it)
        return ''.join(chars)
