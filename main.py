import sys, re, math, time
import numpy as np
from data_structures import UnionFind, MinBinHeap, LinkedList
constraintsFile = None
preferencesFile = None
experiment = 0

class Constraints:
    def __init__(self, constraints_raw):
        self.numTimes = int(constraints_raw[0].split('\t')[-1])
        cur = 1
        while not constraints_raw[cur].startswith('Room'):
            cur += 1
        self.numRooms = int(constraints_raw[cur].split('\t')[-1])
        cur += 1
        self.rooms = []
        self.teachers = []
        self.IDtoCourse = {}
        self.CoursetoID = {}
        if not re.match("[0-9]+", constraints_raw[cur]): # we dont have nums
            while not constraints_raw[cur].startswith('Classes'):
                self.rooms.append((constraints_raw[cur].split('\t')[0],int(constraints_raw[cur].split('\t')[1])))
                cur += 1
        else:
            while re.match("[0-9]+", constraints_raw[cur]):
                self.rooms.append((int(constraints_raw[cur].split('\t')[0]),int(constraints_raw[cur].split('\t')[1])))
                cur += 1
        self.numClass = int(constraints_raw[cur].split('\t')[-1])
        cur += 1
        self.numTeach = int(constraints_raw[cur].split('\t')[-1])
        cur += 1
        randTeach = -1
        id = 1
        while re.search("[0-9]+", constraints_raw[cur]):
            t = constraints_raw[cur].split('\t')[1]
            if t == '':
                t = randTeach
                randTeach -= 1
            crs = int(constraints_raw[cur].split('\t')[0])
            #self.teachers.append((int(constraints_raw[cur].split('\t')[0]),int(t)))
            self.teachers.append((id,int(t)))
            # Map 1 - numclasses to the course ID (if it isn't contiguous)
            self.IDtoCourse[id] = crs
            self.CoursetoID[crs] = id
            cur += 1
            id += 1

    def __str__(self):
        return str(self.rooms) + '\n' + str(self.teachers)

class Preferences:
    def __init__(self, preferences_raw, CtoID, IDtoC):
        self.ptr = 0
        self.numStudents = int(preferences_raw[0].split('\t')[-1])
        self.prefLists = []
        self.maxPref = 0
        self.CtoID = CtoID
        self.IDtoC = IDtoC
        cur = 1
        thePrefs = []
        while re.match("[0-9]+", preferences_raw[cur]):
            stud = int(preferences_raw[cur].split('\t')[0])
            prefs = re.sub('.*\t','',preferences_raw[cur]).rstrip().split(' ')
            # convert courses to their IDs 
            modifiedPref = ((stud, [CtoID[int(pref)] for pref in prefs if int(pref) in CtoID])) # I hate this way of doing it but whatever
            self.maxPref += len(modifiedPref[1])
            thePrefs.append(modifiedPref)
            cur += 1
        self.prefLists = thePrefs
    def __str__(self):
        return str(self.prefLists)

def sortMajor(Prefs, majorKey, minorKey, subjKey):
    preflist = Prefs.prefLists
    CtoID = Prefs.CtoID
    IDtoC = Prefs.IDtoC
    newPrefs = []
    newMax = 0
    for stud, courses in preflist:
        mjr = []
        mnr = []
        rest = []
        major = majorKey[stud]
        minor = minorKey[stud]
        priority = 1
        for c in courses:
            newMax += priority
            if IDtoC[c] in subjKey[major]:
                mjr.append(c)
            else:
                if IDtoC[c] in subjKey[minor]:
                    mnr.append(c)
                else:
                    rest.append(c)
            priority += 1
        newcourses = mjr + mnr + rest
        newPrefs.append((stud, newcourses))
    Prefs.prefLists = newPrefs
    Prefs.maxPref = newMax
    return Prefs

def parseMajor(Cons, Prefs):
    majorKey = {}
    minorKey = {}
    subjKey = {}
    majors = open(sys.argv[4], 'r').read().split('\n')
    cur = 1 # majors
    while not re.search("subjects", majors[cur]):
        # studentNum    "major" "minor"
        stud = int(majors[cur].split('\t')[0])
        majmin = majors[cur].split('\t')[1].split(' ')
        maj = majmin[0]
        if len(majmin) > 1: #we have a minor
            min = majmin[1]
        majorKey[stud] = maj
        minorKey[stud] = min
        cur += 1
    cur += 1 # subjects
    while majors[cur] != "":
        subj = majors[cur].split('\t')[0]
        courses = [int(c) for c in (majors[cur].split('\t')[1]).split(' ')]
        subjKey[subj] = courses
        cur += 1
    sortedPref = sortMajor(Prefs, majorKey, minorKey, subjKey)
    return Cons, sortedPref

def parse_special(Cons, Prefs):
    if sys.argv[3] == "--major":
        return parseMajor(Cons, Prefs)
    
def parse_args():
    # find the constraints file
    # find the preferences file
    # from sys.argv
    constraintsFile = sys.argv[1] 
    preferencesFile = sys.argv[2]
    constraints_raw = open(constraintsFile, 'r').read().split('\n')
    preferences_raw = open(preferencesFile, 'r').read().split('\n')
    Cons = Constraints(constraints_raw)
    CtoID = Cons.CoursetoID
    IDtoC = Cons.IDtoCourse
    flag = ""
    Prefs = Preferences(preferences_raw, CtoID, IDtoC)
    if len(sys.argv) > 3: # we have special constraints to add
        flag = sys.argv[3]
        Cons, Prefs = parse_special(Cons, Prefs)
    return flag, Cons, Prefs

def setTeach(M, teachers):
    teachers.sort(key=lambda tup: tup[1]) # sort by the teacher
    last = teachers[0]
    i = 1
    thisTeach = [last[0]] # the first course
    while i < len(teachers):
        teach = teachers[i]
        if teach[1] == last[1]: # same teacher
            thisTeach.append(teach[0])
        else: # we have just encountered a new teacher, set inf for the last set
            for ci in range(0, len(thisTeach)):
                for cj in range(ci, len(thisTeach)):
                    c1 = min(thisTeach[ci], thisTeach[cj])
                    c2 = max(thisTeach[ci], thisTeach[cj])
                    M[c1-1,c2-1] = float('inf')
            thisTeach = [teach[0]] # first class of the new teacher
        last = teach
        i+=1
    return M

def setCost(M, preferences):
    for studentTup in preferences:
        prefs = studentTup[1]
        n = len(prefs)
        for i in range(0,n):
            for j in range(i+1,n):
                id1 = prefs[i]
                id2 = prefs[j]
                c1 = min(id1, id2)
                c2 = max(id1, id2)
                M[id1-1,id2-1]+=1
    return M


def setCostSorted(M, preferences):
    for studentTup in preferences:
        prefs = studentTup[1]
        n = len(prefs)
        for i in range(0,n):
            for j in range(i+1,n):
                id1 = prefs[i]
                id2 = prefs[j]
                c1 = min(id1, id2)
                c2 = max(id1, id2)
                M[id1-1,id2-1]+=(n-i)+(n-j)
    return M

def createSets(M,numClasses,numRooms,numTimes):
    heapSize = 0
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
        startNum = timeGroups.numSets
        try:
            ID1, ID2, conflictScore = groupConflicts.pop()
            heapSize -= 1
        except AttributeError as e:
            print (timeGroups.groups())
            print ()
            raise e
        rep1, rep2 = groupReps[ID1], groupReps[ID2]
        if rep1 is None or rep2 is None:
            pass
        elif timeGroups.find(rep1) == timeGroups.find(rep2):
            pass
        else:
            #print(timeGroups.find(13), timeGroups.find(19))
            timeGroups.union(rep2,rep1)
            if timeGroups.numSets != startNum:
            # this is the adding together rows and columns thingy
                groups = [nextID]
                for i in range(numClasses):
                    M[min(rep1-1,timeGroups.find(i+1)-1)][max(rep1-1,timeGroups.find(i+1)-1)] += M[min(rep2-1,timeGroups.find(i+1)-1)][max(rep2-1,timeGroups.find(i+1)-1)]
                    #M[min(rep1-1,i)][max(rep1-1,i)] += M[min(rep2-1,i)][max(rep2-1,i)]
                for i in range(numClasses):
                    otherGroupID = groupIDs[timeGroups.find(i+1)]
                    if otherGroupID not in groups:
                        confl = M[min(rep1-1,timeGroups.find(i+1)-1)][max(rep1-1,timeGroups.find(i+1)-1)]
                        #confl = M[min(rep1-1,i)][max(rep1-1,i)]
                        toPush = (nextID, otherGroupID, confl)
                        groupConflicts.push((nextID, otherGroupID, confl))
                        heapSize += 1
                        groups.append(otherGroupID)

                groupReps[nextID] = rep1
                groupReps[ID1] = None
                groupReps[ID2] = None

                groupIDs[rep1] = nextID
                groupIDs[rep2] = nextID
                nextID += 1
            
    #print(timeGroups.groups())
    return timeGroups.groups()

def createSchedule(teachers, classGroups, prefMaster, roomList, n):
    #create empty schedule
    # Note that at this point, courses are represented by IDs, unpack in formatSchedule
    schedule = {}
    for (course, prof) in teachers:
        schedule[course] = {'room':0, 'teacher':0, 'time':0, 'students':[]}
    #assign teachers to courses
    for (course, prof) in teachers:
        schedule[course]['teacher'] = prof
    #assign times so that grouped courses are at the same time
    for idx2,group in enumerate(classGroups, 1):
        for course in group:
            schedule[course]['time'] = idx2
    #fill out students for each course, assuming all can fit
    for preflist in prefMaster:
        idx = preflist[0]
        prefs = preflist[1]
        times = []
        for course in prefs:
            if schedule[course]['time'] not in times:
                times.append(schedule[course]['time'])
                schedule[course]['students'].append(idx)
    #assign times and rooms to courses (bigger classes get bigger rooms)
    sorted_rooms = sorted(roomList, key=lambda kv: kv[1], reverse=True)
    for group in classGroups:
        sorted_group = sorted(group, key=lambda c: len(schedule[c]['students']), reverse=True)
        for idx3,course in enumerate(sorted_group):
                schedule[course]['room'] = sorted_rooms[idx3][0]
    #make sure there are not more students in the class than the room it is assigned to can fit
    roomDict = dict(roomList)
    for course in range(1, n+1):
        if(len(schedule[course]['students']) > roomDict[schedule[course]['room']]):
            #remove the students that don't fit from the end of the 'students' list for this course
            #NOTE: This repetitively shortchanges higher-numbered students, because we remove students we can't handle from the END of the list.
            schedule[course]['students'] = schedule[course]['students'][0:roomDict[schedule[course]['room']]]
    return schedule

def formatSchedule(schedule, n, IDtoC, numTeach):
    f = open('schedule.txt', 'w+')
    
    f.write('Course\tRoom\tTeacher\tTime\tStudents\n')
    for course in range(1, n+1):
        students = [str(stud) for stud in schedule[course]['students']]
        teacher = schedule[course]['teacher']
        if teacher < 0:
            pass
        else:
            f.write('{0}\t{1}\t{2}\t{3}\t{4}\n'.format(str(IDtoC[course]), str(schedule[course]['room']), str(teacher), str(schedule[course]['time']), ' '.join(students)))
    f.close()

def main():
    start = time.time()
    flag, constraints, preferences= parse_args()
    teachers = constraints.teachers
    numTeach = constraints.numTeach
    CtoID = constraints.CoursetoID
    IDtoC = constraints.IDtoCourse
    n = int(constraints.numClass)
    M = np.zeros((n,n))
    M = setTeach(M, teachers)
    if flag == "--major" or flag == "--dist":
        M = setCostSorted(M, preferences.prefLists)
    else:
        M = setCost(M, preferences.prefLists)
    classGroups = createSets(M,n,constraints.numRooms,constraints.numTimes)
    schedule = createSchedule(teachers, classGroups, preferences.prefLists, constraints.rooms, n)
    formatSchedule(schedule, n, IDtoC, numTeach)
    print("Best preferences value: {0}".format(preferences.maxPref))
    print("--- %s seconds ---" % (time.time() - start))

# note that everything is 1-indexed, but we are keeping the matrix zero-indexed, so decrement when u store and increment when you restore

if __name__ == "__main__":
    main()