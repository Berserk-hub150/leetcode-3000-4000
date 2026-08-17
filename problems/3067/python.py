from typing import List


class Solution:
    def countPairsOfConnectableServers(self, edges: List[List[int]], signalSpeed: int) -> List[int]:
        n = len(edges) + 1
        graph = [[] for _ in range(n)]
        for u, v, weight in edges:
            graph[u].append((v, weight))
            graph[v].append((u, weight))

        def count_branch(node: int, parent: int, distance: int) -> int:
            count = int(distance % signalSpeed == 0)
            for nxt, weight in graph[node]:
                if nxt != parent:
                    count += count_branch(nxt, node, distance + weight)
            return count

        answer = [0] * n
        for center in range(n):
            previous = 0
            for neighbor, weight in graph[center]:
                current = count_branch(neighbor, center, weight)
                answer[center] += previous * current
                previous += current
        return answer
