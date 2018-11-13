import sys, re, math, time
import numpy as np
from data_structures import UnionFind, MinBinHeap, LinkedList
constraintsFile = None
preferencesFile = None
experiment = 0

class Constraints:
    def __init__(self, constraints_raw):
        self.numTimes = int(constraints_raw[0].split('\t')[-1])
        self.numRooms = int(constraints_raw[1].split('\t')[-1])
        self.rooms = []
        self.teachers = []
        cur = 2
        while re.match("[0-9]+", constraints_raw[cur]):
            self.rooms.append((int(constraints_raw[cur].split('\t')[0]),int(constraints_raw[cur].split('\t')[1])))
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
    experiment = sys.argv[3]
    constraints_raw = open(constraintsFile, 'r').read().split('\n')
    preferences_raw = open(preferencesFile, 'r').read().split('\n')
    return Constraints(constraints_raw), Preferences(preferences_raw), experiment

def setTeach(M, teachers):
    teachers.sort(key=lambda tup: tup[1]) # sort by the teacher
    #print(teachers)
    last = teachers[0]
    i = 1
    while i < len(teachers):
        teach = teachers[i]
        if teach[1] == last[1]: # same teacher
            c1 = min(teach[0],last[0])
            c2 = max(teach[0],last[0])
            M[c1-1,c2-1] = float('inf')
        last = teachers[i]
        i+=1
    return M

def setCost(M, preferences):
    for student in preferences:
        for i in range(0,4):
            for j in range(i+1,4):
                c1 = min(student[i], student[j])
                c2 = max(student[i], student[j])
                M[c1-1,c2-1]+=(4-i)+(4-j)
    #print(M)
    return M

def createSets(M,numClasses,numRooms,numTimes):
    #print(M)
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
            #print((ID1+1,ID2+1,M[ID1,ID2]))
            heapSize += 1
            groupConflicts.push((ID1+1,ID2+1,M[ID1,ID2]))
    
    while timeGroups.numSets > numTimes:

        try:
            ID1, ID2, conflictScore = groupConflicts.pop()
            heapSize -= 1
        except AttributeError as e:
            print (timeGroups.groups())
            raise e
        rep1, rep2 = groupReps[ID1], groupReps[ID2]
        if rep1 is None or rep2 is None:
            pass
        elif timeGroups.find(rep1) == timeGroups.find(rep2):
            pass
            '''
        else:
            #print(timeGroups.groups())
            rep1, rep2 = timeGroups.find(rep1), timeGroups.find(rep2) # just in case
            #if rep1 in [2,12] and rep2 in [2,12]:
                #print(M)
            #print(conflictScore)
            timeGroups.union(rep2, rep1)
            for i in range(numClasses):
                M[min(rep1-1,i)][max(rep1-1,i)] += M[min(rep2-1,i)][max(rep2-1,i)]
            for set in timeGroups.groups():
                thisrep = timeGroups.find(list(set)[0])
                if not timeGroups.issame(rep1, thisrep):
                    confl = M[min(rep1-1,thisrep-1)][max(rep1-1,thisrep-1)]
                    otherGroupID = groupIDs[thisrep]
                    groupConflicts.push((nextID, otherGroupID, confl))

            groupReps[nextID] = rep1
            groupReps[ID1] = None
            groupReps[ID2] = None

            groupIDs[rep1] = nextID
            groupIDs[rep2] = nextID
            nextID += 1
            '''
        else:
            #print(timeGroups.find(13), timeGroups.find(19))
            timeGroups.union(rep2,rep1)
            # this is the adding together rows and columns thingy
            groups = [nextID]
            for i in range(numClasses):
                M[min(rep1-1,timeGroups.find(i+1)-1)][max(rep1-1,timeGroups.find(i+1)-1)] += M[min(rep2-1,timeGroups.find(i+1)-1)][max(rep2-1,timeGroups.find(i+1)-1)]
                #M[min(rep1-1,i)][max(rep1-1,i)] += M[min(rep2-1,i)][max(rep2-1,i)]
            #print(M)
            for i in range(numClasses):
                otherGroupID = groupIDs[timeGroups.find(i+1)]
                if otherGroupID not in groups:
                    confl = M[min(rep1-1,timeGroups.find(i+1)-1)][max(rep1-1,timeGroups.find(i+1)-1)]
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
            
    print(timeGroups.groups())
    return timeGroups.groups()


    '''
        else:
            #print(timeGroups.find(13), timeGroups.find(19))
            timeGroups.union(rep2,rep1)
            # this is the adding together rows and columns thingy
            #groups = []
            for i in range(numClasses):
                M[min(rep1-1,timeGroups.find(i+1)-1)][max(rep1-1,timeGroups.find(i+1)-1)] += M[min(rep2-1,timeGroups.find(i+1))][max(rep2-1,timeGroups.find(i+1)-1)]
            for set in timeGroups.groups():
                thisrep = timeGroups.find(list(set)[0])
                otherGroupID = groupIDs[thisrep]
                confl = M[min(rep1-1, thisrep-1)][max(rep1-1, thisrep-1)]
                groupConflicts.push((nextID, otherGroupID, confl))

            groupReps[nextID] = rep1
            groupReps[ID1] = None
            groupReps[ID2] = None

            groupIDs[rep1] = nextID
            groupIDs[rep2] = nextID
            nextID += 1
            if rep2 == 13:
                print("after 13 is merged into 6, and 19 conflict with ", M[5][18])
        '''

def createSchedulePrev(teachers, classGroups, prefMaster, roomList, n):
    #create empty schedule
    schedule = {}
    for course in range(1, n+1):
        schedule[course] = {'room':0, 'teacher':0, 'time':0, 'students':[]}
    #assign teachers to courses
    for (course, prof) in teachers:
        schedule[course]['teacher'] = prof
    #fill out students for each course, assuming infinite classroom size
    for idx,preflist in enumerate(prefMaster, 1):
        for course in preflist:
            schedule[course]['students'].append(idx)
    #assign times and rooms to courses (bigger classes get bigger rooms)
    #sorted_* means that the item is sorted for maximum student attendance first (larger rooms first, larger classes first)
    sorted_rooms = sorted(roomList, key=lambda kv: kv[1], reverse=True)
    sorted_schedule = sorted(schedule.items(), key=lambda kv: len(kv[1]['students']), reverse=True)
    sorted_courses = [elem[0] for elem in sorted_schedule]
    for idx2,group in enumerate(classGroups, 1):
        sorted_group = [elem for elem in sorted_courses if elem in group]
        for idx3,course in enumerate(sorted_group):
            schedule[course]['time'] = idx2
            schedule[course]['room'] = sorted_rooms[idx3][0]
    #make sure there are not more students in the class than the room it is assigned to can fit
    roomDict = dict(roomList)
    for course in range(1, n+1):
        if(len(schedule[course]['students']) > roomDict[schedule[course]['room']]):
            #remove the students that don't fit from the end of the 'students' list for this course
            #NOTE: This repetitively shortchanges higher-numbered students, because we remove students we can't handle from the END of the list.
            schedule[course]['students'] = schedule[course]['students'][0:roomDict[schedule[course]['room']]]
    return schedule


def createSchedule(teachers, classGroups, prefMaster, roomList, n):
    #create empty schedule
    #print(classGroups)
    schedule = {}
    for course in range(1, n+1):
        schedule[course] = {'room':0, 'teacher':0, 'time':0, 'students':[]}
    #assign teachers to courses
    for (course, prof) in teachers:
        schedule[course]['teacher'] = prof
    #assign times so that grouped courses are at the same time
    for idx2,group in enumerate(classGroups, 1):
        for course in group:
            schedule[course]['time'] = idx2
    #fill out students for each course, assuming all can fit
    for idx,preflist in enumerate(prefMaster, 1):
        times = []
        for course in preflist:
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

def formatSchedule(schedule, n, experiment):
    f = open('schedule_{0}.txt'.format(experiment), 'w+')
    
    f.write('Course\tRoom\tTeacher\tTime\tStudents\n')
    for course in range(1, n+1):
        students = [str(stud) for stud in schedule[course]['students']]
        f.write('{0}\t{1}\t{2}\t{3}\t{4}\n'.format(str(course), str(schedule[course]['room']), str(schedule[course]['teacher']), str(schedule[course]['time']), ' '.join(students)))
    f.close()

def main():
    start = time.time()
    constraints, preferences, experiment = parse_args()
    teachers = constraints.teachers
    n = int(constraints.numClass)
    M = np.zeros((n,n))
    M = setTeach(M, teachers)
    #print(M)
    M = setCost(M, preferences.prefLists)
    classGroups = createSets(M,n,constraints.numRooms,constraints.numTimes)
    schedule = createSchedule(teachers, classGroups, preferences.prefLists, constraints.rooms, n)
    formatSchedule(schedule, n, experiment)
    print("--- %s seconds ---" % (time.time() - start))

# note that everything is 1-indexed, but we are keeping the matrix zero-indexed, so decrement when u store and increment when you restore

if __name__ == "__main__":
    main()