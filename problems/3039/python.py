from collections import Counter


class Solution:
    def lastNonEmptyString(self, s: str) -> str:
        freq = Counter(s)
        highest = max(freq.values())
        last = {}
        for i, ch in enumerate(s):
            last[ch] = i
        survivors = [ch for ch, count in freq.items() if count == highest]
        survivors.sort(key=last.__getitem__)
        return "".join(survivors)
