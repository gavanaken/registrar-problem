import csv

Subjects = {}
Levels = {}

with open('haverfordEnrollmentDataS14.csv', 'r') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    results = []
    courses = {}
    departments = {}
    cur = '1'
    depts = []
    for row in csv_reader: #skip headers
        if row[0] == 'Student':
            pass
        else:
            if row[2] not in Subjects:
                Subjects[row[2]] = [row[1]]
            else:
                if row[1] not in Subjects[row[2]]:
                    Subjects[row[2]].append(row[1])
            if row[4] not in Levels:
                Levels[row[4]] = [row[1]]
            else:
                if row[1] not in Levels[row[4]]:
                    Levels[row[4]].append(row[1])

#print(Subjects)
#print(Levels)

output = 'subjects\n'
for k in Subjects:
    output = output + k + '\n'
    for c in Subjects[k]:
        output = output + c + '\n'
output = output + 'levels\n'
for k in Levels:
    output = output + 'level ' + k + '\n'
    for c in Levels[k]:
        output = output + c + '\n'

with open('DeptLevels.txt', 'w+') as outputFile:
    outputFile.write(output)



