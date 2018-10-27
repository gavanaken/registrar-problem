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

if __name__ == "__main__":
    pairs = [(0,9),(1,8),(2,7),(3,6),(4,5),(5,4),(6,3),(7,2),(8,1),(9,0)]
    mbh0 = MinBinHeap(pairs, key=lambda x: x[0])
    mbh1 = MinBinHeap(pairs, key=lambda x: x[1])
    print(mbh0)
    print(mbh1)
