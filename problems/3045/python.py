from typing import List


class TrieNode:
    __slots__ = ("children", "terminal")

    def __init__(self):
        self.children = {}
        self.terminal = 0


class Solution:
    def countPrefixSuffixPairs(self, words: List[str]) -> int:
        root = TrieNode()
        answer = 0
        for word in words:
            node = root
            n = len(word)
            for i in range(n):
                key = (word[i], word[n - 1 - i])
                node = node.children.setdefault(key, TrieNode())
                answer += node.terminal
            node.terminal += 1
        return answer
