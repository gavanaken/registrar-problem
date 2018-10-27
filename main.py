import sys, re, math
import numpy as np
from unionfind import UnionFind
from heap import MinBinHeap
constraintsFile = None
preferencesFile = None

class Constraints:
    def __init__(self, constraints_raw):
        self.numTimes = int(constraints_raw[0][-1])
        self.numRooms = int(constraints_raw[1][-1])
        self.rooms = []
        self.teachers = []
        cur = 2
        while re.match("[0-9]+", constraints_raw[cur]):
            self.rooms.append(constraints_raw[cur].split('\t')[1])
            cur += 1
        self.numClass = int(constraints_raw[cur].split('\t')[-1])
        cur += 1
        self.numTeach = int(constraints_raw[cur].split('\t')[-1])
        cur += 1
        while re.search("[0-9]+", constraints_raw[cur]):
            self.teachers.append((int(constraints_raw[cur].split('\t')[0]),int(constraints_raw[cur].split('\t')[1])))
            cur += 1

    def __str__(self):
        return str(self.rooms) + '\n' + str(self.teachers)

class Preferences:
    def __init__(self, preferences_raw):
        self.ptr = 0
        self.numStudents = int(preferences_raw[0].split('\t')[-1])
        self.prefLists = []
        cur = 1
        while re.match("[0-9]+", preferences_raw[cur]):
            prefs = re.sub('.*\t','',preferences_raw[cur]).split(' ')
            self.prefLists.append([int(pref) for pref in prefs]) # I hate this way of doing it but whatever
            cur += 1
    def __str__(self):
        return str(self.prefLists)
    
def parse_args():
    # find the constraints file
    # find the preferences file
    # from sys.argv
    constraintsFile = sys.argv[1] 
    preferencesFile = sys.argv[2]
    constraints_raw = open(constraintsFile, 'r').read().split('\n')
    preferences_raw = open(preferencesFile, 'r').read().split('\n')
    return Constraints(constraints_raw), Preferences(preferences_raw)

def setTeach(M, teachers):
    teachers.sort(key=lambda tup: tup[1]) # sort by the teacher
    last = teachers[1]
    i = 1
    while i < len(teachers):
        teach = teachers[i]
        if teach[1] == last[1]: # same teacher
            c1 = min(teach[0],last[0])
            c2 = max(teach[0],last[0])
            M[c1-1,c2-1] = 1000 #math.inf
        last = teachers[i]
        i+=1
    return M

def setCost(M, preferences):
    for student in preferences:
        for i in range(0,4):
            for j in range(i+1,4):
                c1 = min(student[i], student[j])
                c2 = max(student[i], student[j])
                #print(c1, c2)
                M[c1-1,c2-1]+=(4-i)+(4-j)
    return M

def createSets(M,numClasses,numRooms,numTimes):
    S = UnionFind([i+1 for i in range(numClasses)],numRooms)
    P = MinBinHeap(key=lambda x: x[2])
    for i in range(0,numClasses-1):
        for j in range(i+1,numClasses):
            P.push((i+1,j+1,M[i,j]))
    while S.numSets > numTimes:
        i, j, conflictScore = P.pop()
        print(i,j,conflictScore)
        S.union(i,j)

    return S.groups()

def main():
    constraints, preferences = parse_args()
    teachers = constraints.teachers
    n = int(constraints.numClass)
    M = np.zeros((n,n))
    M = setTeach(M, teachers)
    M = setCost(M, preferences.prefLists)
    classGroups = createSets(M,n,constraints.numRooms,constraints.numTimes)
    print(classGroups)

# note that everything is 1-indexed, but we are keeping the matrix zero-indexed, so decrement when u store and increment when you restore

if __name__ == "__main__":
    main()
