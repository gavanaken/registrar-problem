class MinBinHeap:
    def __init__(self,s):
        self.root = None
        for item in s:
            self.push(item)

    def push(self,item):
        if self.root is None:
            self.root = MinBinNode(item)
        else:
            self.root.push(item)

    def pop(self):
        out, self.root = self.root.pop()
        return out

    def __str__(self):
        lines = self.root.lines() if self.root else [""]
        return("\n".join(lines))

class MinBinNode:
    def __init__(self,_val):
        self.val = _val
        self.right = None
        self.left = None
        self.balance = 0

    def push(self,newval):
        if self.val < newval:
            to_push = newval
        else:
            to_push = self.val
            self.val = newval

        if self.left is None:
            self.left = MinBinNode(to_push)
            self.balance -= 1
        elif self.right is None:
            self.right = MinBinNode(to_push)
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
        elif self.left.val < self.right.val:
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
