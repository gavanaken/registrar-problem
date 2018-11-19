import sys, re

preferences_raw = open(sys.argv[1], 'r').read().split('\n')
prefDict = {}
cur = 1
while re.match("[0-9]+", preferences_raw[cur]):
    stud = int(preferences_raw[cur].split('\t')[0])
    prefs = re.sub('.*\t','',preferences_raw[cur]).rstrip().split(' ')
    # convert courses to their IDs 
    prefDict[stud] = [int(pref) for pref in prefs] # I hate this way of doing it but whatever
    cur += 1


weightsFile = sys.argv[2]
# weights file is just:
# student   weight1 weight2 weight3
# corresponding to course1 course2 course3
weightlines = open(weightsFile, 'r').read().split('\n')
theWeights = {}
newMax = 0
for w in weightlines[1:]: # skip the header
    if w != '': #make sure there aren't trailing newlines
        stud = int(w.split('\t')[0])
        weights = [int(wt) for wt in w.split('\t')[1].split(' ')]
        theWeights[stud] = weights
        newMax += 10 # each student gets 10 preference units to distribute


prefVal = 0

schedule = open(sys.argv[3], 'r').read().split('\n')
for crs in schedule[1:]:
    if crs != '':
        course = int(crs.split('\t')[0])
        students = crs.split('\t')[4].split(' ')
        for s in students:
            if s != '':
                prefVal += theWeights[int(s)][prefDict[int(s)].index(course)]

print ("Student preferences value: {0}".format(str(prefVal)))