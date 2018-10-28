class MinBinHeap:
    def __init__(self,s=[],key=lambda x: x):
        self.root = None
        self.key = key
        for item in s:
            self.push(item)

    def push(self,item):
        if self.root is None:
            self.root = MinBinNode(item,self.key)
        else:
            self.root.push(item)

    def pop(self):
        out, self.root = self.root.pop()
        return out

    def __str__(self):
        lines = self.root.lines() if self.root else [""]
        return("\n".join(lines))

class MinBinNode:
    def __init__(self,val,key):
        self.val = val
        self.key = key
        self.right = None
        self.left = None
        self.balance = 0

    def push(self,newval):
        if self.key(self.val) < self.key(newval):
            to_push = newval
        else:
            to_push = self.val
            self.val = newval

        if self.left is None:
            self.left = MinBinNode(to_push, self.key)
            self.balance -= 1
        elif self.right is None:
            self.right = MinBinNode(to_push, self.key)
            self.balance += 1
        elif self.balance >= 0:
            self.left.push(to_push)
            self.balance -= 1
        else:
            self.right.push(to_push)
            self.balance += 1

    def pop(self):
        out = self.val
        if self.left is None and self.right is None:
            return out, None
        elif self.left is None:
            self.val, self.right = self.right.pop()
            self.balance -= 1
        elif self.right is None:
            self.val, self.left = self.left.pop()
            self.balance += 1
        elif self.key(self.left.val) < self.key(self.right.val):
            self.val, self.left = self.left.pop()
            self.balance += 1
        else:
            self.val, self.right = self.right.pop()
            self.balance -= 1
        return out, self

    def lines(self):
        leftlines = [] if self.left is None else self.left.lines()
        rightlines = [] if self.right is None else self.right.lines()
        if len(leftlines) < len(rightlines):
            for i in range(len(leftlines),len(rightlines)):
                leftlines.append(" "*(0 if leftlines == [] else len(leftlines[0])))
        else:
            for i in range(len(rightlines),len(leftlines)):
                rightlines.append(" "*(0 if rightlines == [] else len(rightlines[0])))
        combined = [leftlines[i] + rightlines[i] for i in range(len(leftlines))]
        l = 0 if combined == [] else len(combined[0])
        s = str(self.val).ljust(l," ")
        combined = [s] + combined
        return combined

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

class LinkedList:
    def __init__(self,l=[]):
        self.head = None
        self.tail = None
        for item in l:
            self.append(item)

    def create(self,item):
        n = LinkedNode(item)
        self.head = n
        self.tail = n
        n.prev = None
        n.next = None
        
    def append(self,item):
        if self.head is None:
            self.create(item)
        else:
            n = LinkedNode(item)
            self.tail.next = n
            n.prev = self.tail
            n.next = None
            self.tail = n

    def prepend(self,item):
        if self.head is None:
            self.create(item)
        else:
            n = LinkedNode(item)
            self.head.prev = n
            n.next = self.head
            n.prev = None
            self.head = n

    def pophead(self):
        out = self.head.val
        self.head.next.prev = None
        self.head = self.head.next
        return out

    def poptail(self):
        out = self.tail.val
        self.tail.prev.next = None
        self.tail = self.tail.prev
        return out

    def __repr__(self):
        l = []
        n = self.head
        while n:
            l.append(n.val)
            n = n.next
        return "LinkedList(%s)" % str(l)

class LinkedNode:
    def __init__(self,val):
        self.val = val
        self.prev = None
        self.next = None

    def __repr__(self):
        return "LinkedNode(%s)" % self.val.__repr__()

if __name__ == "__main__":
    pairs = [(0,9),(1,8),(2,7),(3,6),(4,5),(5,4),(6,3),(7,2),(8,1),(9,0)]
    mbh0 = MinBinHeap(pairs, key=lambda x: x[0])
    mbh1 = MinBinHeap(pairs, key=lambda x: x[1])
    print(mbh0)
    print(mbh1)

    # this corner case demonstrates how a single find operation can take O(n)
    uf = UnionFind({"hells","bells","back","in","black"})
    print(uf.parent)
    for i in range(len(uf.valuesl)-1):
            uf.union(uf.valuesl[i],uf.valuesl[i+1])
            print(uf.parent)
    uf.find(uf.valuesl[0])
    print(uf.parent)

    ll = LinkedList([0,1,2,3,4,5,])
