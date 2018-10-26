import sys, re, math
import numpy as np
import unionfind
constraintsFile = None
preferencesFile = None

class Constraints:

    def __init__(self, constraints_raw):
        self.numTimes = constraints_raw[0][-1]
        self.numRooms = constraints_raw[1][-1]
        self.rooms = []
        self.teachers = []
        cur = 2
        while re.match("[0-9]+", constraints_raw[cur]):
            self.rooms.append(constraints_raw[cur].split('\t')[1])
            cur += 1
        self.numClass = constraints_raw[cur].split('\t')[-1]
        cur += 1
        self.numTeach = constraints_raw[cur].split('\t')[-1]
        cur += 1
        while re.search("[0-9]+", constraints_raw[cur]):
            self.teachers.append((constraints_raw[cur].split('\t')[0],constraints_raw[cur].split('\t')[1]))
            cur += 1

    def __str__(self):
        return str(self.rooms) + '\n' + str(self.teachers)

class Preferences:

    def __init__(self, preferences_raw):
        self.ptr = 0
        self.numStudents = preferences_raw[0].split('\t')[-1]
        self.prefLists = []
        cur = 1
        while re.match("[0-9]+", preferences_raw[cur]):
            self.prefLists.append(re.sub('.*\t','',preferences_raw[cur]).split(' ')) # I hate this way of doing it but whatever
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
    teachers.sort(key=lambda tup: tup[0]) # sort by the teacher
    last = teachers[0]
    i = 1
    while i < len(teachers):
        teach = teachers[i]
        if teach[0] == last[0]: # same teacher
            M[teach[1]-1,last[1]-1] = math.inf
        last = teachers[i]
        i+=1
    return M

def setCost(M, preferences):
    print(preferences)
    for student in preferences:
        for i in range(0,4):
            for j in range(i+1,4):
                c1 = min(int(student[i]), int(student[j]))
                c2 = max(int(student[i]), int(student[j]))
                #print(c1, c2)
                M[c1-1,c2-1]+=(4-i)+(4-j)
    return M


def main():
    constraints, preferences = parse_args()
    teachers = constraints.teachers
    n = int(constraints.numClass)
    M = np.zeros((n,n))
    M = setTeach(M, teachers)
    print(M)
    M = setCost(M, preferences.prefLists)
    print(M)

    



# note that everything is 1-indexed, but we are keeping the matrix zero-indexed, so decrement when u store and increment when you restore

if __name__ == "__main__":
    main()