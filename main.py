import sys, re, math
import numpy as np
from data_structures import UnionFind, MinBinHeap, LinkedList
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
    timeGroups = UnionFind([i+1 for i in range(numClasses)],numRooms)
    groupConflicts = MinBinHeap(key=lambda x: x[2])
    nextID = numClasses+1
    
    groupReps = [0]*(numClasses*2)
    for i in range(1,numClasses+1):
        groupReps[i] = i
    groupIDs = [0]*(numClasses+1)
    for i in range(1,numClasses+1):
        groupIDs[i] = i
    
    for ID1 in range(0,numClasses-1):
        for ID2 in range(ID1+1,numClasses):
            groupConflicts.push((ID1+1,ID2+1,M[ID1,ID2]))
    
    while timeGroups.numSets > numTimes:
        ID1, ID2, conflictScore = groupConflicts.pop()
        rep1, rep2 = groupReps[ID1], groupReps[ID2]
        if rep1 is None or rep2 is None:
            pass
        elif timeGroups.find(rep1) == timeGroups.find(rep2):
            pass
        else:
            timeGroups.union(rep1,rep2)            
            # this is the adding together rows and columns thingy
            for i in range(numClasses):
                M[min(rep1-1,i)][max(rep1-1,i)] += M[min(rep2-1,i)][max(rep2-1,i)]
                otherGroupID = groupIDs[timeGroups.find(i+1)]
                groupConflicts.push((nextID, otherGroupID, M[min(rep1-1,i)][max(rep1-1,i)]))

            groupReps[nextID] = rep1
            groupReps[ID1] = None
            groupReps[ID2] = None

            groupIDs[rep1] = nextID
            groupIDs[rep2] = nextID
            nextID += 1

    return timeGroups.groups()

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
