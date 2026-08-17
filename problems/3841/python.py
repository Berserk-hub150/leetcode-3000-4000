# Time:  O((n + q) * logn)
# Space: O(n)

# hld, lca, fenwick tree
class Solution(object):
    def palindromePath(self, n, edges, s, queries):
        """
        :type n: int
        :type edges: List[List[int]]
        :type s: str
        :type queries: List[str]
        :rtype: List[bool]
        """
        class BIT(object):  # 0-indexed.
            def __init__(self, n):
                self.__bit = [0]*(n+1)  # Extra one for dummy node.

            def add(self, i, val):
                i += 1  # Extra one for dummy node.
                while i < len(self.__bit):
                    self.__bit[i] ^= val  # modified
                    i += (i & -i)

            def query(self, i):
                i += 1  # Extra one for dummy node.
                ret = 0
                while i > 0:
                    ret ^= self.__bit[i]  # modified
                    i -= (i & -i)
                return ret


        def build_hld(adj, cb):
            parent, depth, size, heavy, head = [-1]*len(adj), [0]*len(adj), [1]*len(adj), [-1]*len(adj), list(range(len(adj)))
            stk = [(1, 0, -1)]
            while stk:
                step, u, p = stk.pop()
                if step == 1:
                    cb(u, p)
                    parent[u], depth[u] = p, (depth[p]+1 if p != -1 else 0)
                    stk.append((2, u, p))
                    for v in adj[u]:
                        if v == p:
                            continue
                        stk.append((1, v, u))
                elif step == 2:
                    for v in adj[u]:
                        if v == parent[u]:
                            continue
                        size[u] += size[v]
                        if heavy[u] == -1 or size[v] > size[heavy[u]]:
                            heavy[u] = v
            idx = -1
            left, right = [-1]*len(adj), [-1]*len(adj)
            stk = [(1, 0, 0)]
            while stk:
                step, u, h = stk.pop()
                if step == 1:
                    idx += 1
                    head[u], left[u] = h, idx
                    stk.append((2, u, h))
                    for v in adj[u]:
                        if v == parent[u] or v == heavy[u]:
                            continue
                        stk.append((1, v, v))
                    if heavy[u] != -1:
                        stk.append((1, heavy[u], h))
                elif step == 2:
                    right[u] = idx
            return parent, depth, head, left, right
    
        def lca(u, v):
            while head[u] != head[v]:
                if depth[head[u]] < depth[head[v]]:
                    u, v = v, u
                u = parent[head[u]]
            return u if depth[u] < depth[v] else v

        def callback(u, p):
            prefix[u] = (prefix[p] if p != -1 else 0)^(1<<(ord(s[u])-ord('a')))

        s = list(s)
        adj = [[] for _ in xrange(n)]
        for u, v in edges:
            adj[u].append(v)
            adj[v].append(u)
        prefix = [0]*n
        parent, depth, head, left, right = build_hld(adj, callback)
        bit = BIT(n+1)
        result = []
        for q in queries:
            args = q.split()
            op = args[0]
            u = int(args[1])
            if op == "update":
                c = args[2]
                diff = (1<<(ord(s[u])-ord('a')))^(1<<(ord(c)-ord('a')))
                if not diff:
                    continue
                s[u] = c
                bit.add(left[u], diff)
                bit.add(right[u]+1, diff)
            else:
                v = int(args[2])
                l = lca(u, v)
                mask = (prefix[u]^bit.query(left[u]))^(prefix[v]^bit.query(left[v]))^(1<<(ord(s[l])-ord('a')))
                result.append((mask&(mask-1)) == 0)
        return result


# Time:  O((n + q) * logn)
# Space: O(nlogn)
# dfs, lca, binary lifting, fenwick tree
class Solution2(object):
    def palindromePath(self, n, edges, s, queries):
        """
        :type n: int
        :type edges: List[List[int]]
        :type s: str
        :type queries: List[str]
        :rtype: List[bool]
        """
        class BIT(object):  # 0-indexed.
            def __init__(self, n):
                self.__bit = [0]*(n+1)  # Extra one for dummy node.

            def add(self, i, val):
                i += 1  # Extra one for dummy node.
                while i < len(self.__bit):
                    self.__bit[i] ^= val  # modified
                    i += (i & -i)

            def query(self, i):
                i += 1  # Extra one for dummy node.
                ret = 0
                while i > 0:
                    ret ^= self.__bit[i]  # modified
                    i -= (i & -i)
                return ret


        class TreeInfos(object):  # Time: O(NlogN), Space: O(NlogN), N is the number of nodes
            def __init__(self, adj):
                N = len(adj)
                L, R, D, P = [0]*N, [0]*N, [0]*N, [[] for _ in xrange(N)]
                idx = -1
                stk = [(1, (0, -1))]
                while stk:
                    step, args = stk.pop()
                    if step == 1:
                        u, p = args
                        D[u] = 1 if p == -1 else D[p]+1
                        if p != -1:
                            P[u].append(p)
                        i = 0
                        while i < len(P[u]) and i < len(P[P[u][i]]):
                            P[u].append(P[P[u][i]][i])
                            i += 1
                        idx += 1
                        L[u] = idx
                        stk.append((2, (u,)))
                        for i in reversed(xrange(len(adj[u]))):
                            v = adj[u][i]
                            if v == p:
                                continue
                            stk.append((1, (v, u)))
                    elif step == 2:
                        u = args[0]
                        R[u] = idx
                assert(idx == N-1)
                self.L, self.R, self.D, self.P = L, R, D, P

            # Template:
            # https://github.com/kamyu104/FacebookHackerCup-2019/blob/master/Final%20Round/little_boat_on_the_sea.py
            def is_ancestor(self, a, b):  # includes itself
                return self.L[a] <= self.L[b] <= self.R[b] <= self.R[a]

            def lca(self, a, b):
                if self.D[a] > self.D[b]:
                    a, b = b, a
                if self.is_ancestor(a, b):
                    return a
                for i in reversed(xrange(len(self.P[a]))):  # O(logN)
                    if i < len(self.P[a]) and not self.is_ancestor(self.P[a][i], b):
                        a = self.P[a][i]
                return self.P[a][0]

        s = list(s)
        adj = [[] for _ in xrange(n)]
        for u, v in edges:
            adj[u].append(v)
            adj[v].append(u)
        tree_infos = TreeInfos(adj)
        bit = BIT(n+1)
        for u in xrange(n):
            diff = 1<<(ord(s[u])-ord('a'))
            bit.add(tree_infos.L[u], diff)
            bit.add(tree_infos.R[u]+1, diff)
        result = []
        for q in queries:
            args = q.split()
            op = args[0]
            u = int(args[1])
            if op == "update":
                c = args[2]
                diff = (1<<(ord(s[u])-ord('a')))^(1<<(ord(c)-ord('a')))
                if not diff:
                    continue
                s[u] = c
                bit.add(tree_infos.L[u], diff)
                bit.add(tree_infos.R[u]+1, diff)
            else:
                v = int(args[2])
                l = tree_infos.lca(u, v)
                mask = bit.query(tree_infos.L[u])^bit.query(tree_infos.L[v])^(1<<(ord(s[l])-ord('a')))
                result.append(mask == 0 or (mask&(mask-1)) == 0)
        return result
