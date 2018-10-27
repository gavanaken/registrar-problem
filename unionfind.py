class UnionFind:
        # _values can be set or list
        def __init__(self, values, maxSetSize = float("inf")):
                assert(len(set(values)) == len(values)) # make sure input has no duplicates
                self.valuesl = list(values)
                self.numSets = len(self.valuesl)
                self.setSizes = [1]*self.numSets
                self.maxSetSize = maxSetSize
                self.parent = list(range(len(self.valuesl)))
                self.valuesd = dict(zip(self.valuesl,self.parent))

        def find(self, v):
                i = self.findindex(self.valuesd[v])
                return self.valuesl[i]

        def findindex(self, i):
                if self.parent[i] != i:
                        self.parent[i] = self.findindex(self.parent[i])
                return self.parent[i]

        def union(self, v, w):
                i = self.valuesd[v]
                j = self.valuesd[w]
                i = self.findindex(i)
                j = self.findindex(j)
                if i != j and (self.setSizes[i] + self.setSizes[j]) <= self.maxSetSize:
                        self.parent[i] = j
                        self.setSizes[j] = self.setSizes[i] + self.setSizes[j]
                        self.setSizes[i] = None
                        self.numSets -= 1

        def issame(self, i, j):
                return self.find(i) == self.find(j)

        def groups(self):
                g = {}
                for i in range(len(self.valuesl)):
                        setID = self.findindex(i)
                        _g = g.get(setID,set())
                        _g.add(self.valuesl[i])
                        g[setID] = _g
                return list(g.values())

        @staticmethod
        def isconnected(l, u = None):
                nw, nh = len(l), len(l[0])
                rw, rh = range(nw), range(nh)
                if not u: u = unionfind(nw * nh)
                f = -1
                for i in rw:
                        for j in rh:
                                if not l[i][j]: continue
                                if f < 0: f = i + j * nw
                                if j > 0 and l[i][j] == l[i][j - 1]: u.union(i + j * nw, i + j * nw - nw)
                                if i > 0 and l[i][j] == l[i - 1][j]: u.union(i + j * nw, i + j * nw - 1)
                                return f >= 0 and all([u.issame(f, i + j * nw) for i in rw for j in rh if l[i][j]])

        @staticmethod
        def isconnectedlist(nw, nh, lst):
                l = [[False] * nw for j in range(nh)]
                for i, j in lst: l[i][j] = True
                return unionfind.isconnected(l)

# this corner case demonstrates how a single find operation can take O(n)
if __name__=="__main__":
        uf = UnionFind({"hells","bells","back","in","black"})
        print(uf.parent)
        for i in range(len(uf.valuesl)-1):
                uf.union(uf.valuesl[i],uf.valuesl[i+1])
                print(uf.parent)
        uf.find(uf.valuesl[0])
        print(uf.parent)
