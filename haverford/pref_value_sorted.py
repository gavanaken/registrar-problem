import sys, re

preferences_raw = open(sys.argv[1], 'r').read().split('\n')
thePrefs = []
cur = 1
while re.match("[0-9]+", preferences_raw[cur]):
    stud = int(preferences_raw[cur].split('\t')[0])
    prefs = re.sub('.*\t','',preferences_raw[cur]).rstrip().split(' ')
    # convert courses to their IDs 
    modifiedPref = ((stud, [int(pref) for pref in prefs])) # I hate this way of doing it but whatever
    thePrefs.append(modifiedPref)
    cur += 1

majorKey = {}
minorKey = {}
subjKey = {}
majors = open(sys.argv[2], 'r').read().split('\n')
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
preflist = thePrefs

prefDict = {}
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
        if c in subjKey[major]:
            mjr.append(c)
        else:
            if c in subjKey[minor]:
                mnr.append(c)
            else:
                rest.append(c)
        priority += 1
    newcourses = mjr + mnr + rest
    prefDict[stud] = newcourses


prefVal = 0

schedule = open(sys.argv[3], 'r').read().split('\n')
for crs in schedule[1:]:
    if crs != '':
        course = crs.split('\t')[0]
        students = crs.split('\t')[4].split(' ')
        for s in students:
            if s != '':
                num = len(prefDict[int(s)])
                prefVal += num - prefDict[int(s)].index(int(course))

print "Student preferences value: ", prefVal