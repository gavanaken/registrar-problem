class unionfind:
        # _values can be set or list
        def __init__(self, _values):
                assert(len(set(_values)) == len(_values)) # make sure input has no duplicates
                self.valuesl = list(_values)
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
                if i != j: self.parent[i] = j

        def issame(self, i, j):
                return self.find(i) == self.find(j)

        def groups(self):
                r = range(len(self.parent))
                return [[j for j in r if self.issame(j, i)] for i in r if i == self.parent[i]]

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
        uf = unionfind({"hells","bells","back","in","black"})
        print(uf.parent)
        for i in range(len(uf.valuesl)-1):
                uf.union(uf.valuesl[i],uf.valuesl[i+1])
                print(uf.parent)
        uf.find(uf.valuesl[0])
        print(uf.parent)
