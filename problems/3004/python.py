from typing import List
import sys


class Solution:
    def maximumSubtreeSize(self, edges: List[List[int]], colors: List[int]) -> int:
        n = len(colors)
        sys.setrecursionlimit(max(1000, n * 2 + 10))
        graph = [[] for _ in range(n)]
        for u, v in edges:
            graph[u].append(v)
            graph[v].append(u)

        answer = 1

        def dfs(node: int, parent: int):
            nonlocal answer
            size = 1
            uniform = True
            for nxt in graph[node]:
                if nxt == parent:
                    continue
                child_size, child_uniform = dfs(nxt, node)
                size += child_size
                if not child_uniform or colors[nxt] != colors[node]:
                    uniform = False
            if uniform:
                answer = max(answer, size)
            return size, uniform

        dfs(0, -1)
        return answer
