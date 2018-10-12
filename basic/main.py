import sys, re

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
            self.rooms.append(re.sub('\t','',constraints_raw[cur]))
            cur += 1
        self.numClass = constraints_raw[cur].split('\t')[-1]
        cur += 1
        self.numTeach = constraints_raw[cur].split('\t')[-1]
        cur += 1
        while re.search("[0-9]+", constraints_raw[cur]):
            self.teachers.append(re.sub('\t','',constraints_raw[cur]))
            cur += 1

    def __str__(self):
        return str(self.rooms) + '\n' + str(self.teachers)

class Preferences:

    def __init__(self, preferences_raw):
        self.numStudents = preferences_raw[0].split('\t')[-1]
        self.prefLists = []
        cur = 1
        while re.match("[0-9]+", preferences_raw[cur]):
            self.prefLists.append(re.sub('\t','',preferences_raw[cur]))
            cur += 1

    def __str__(self):
        return str(self.prefLists)
def parse_args():
    # find the constraints file
    # find the preferences file
    # from sys.argv
    return sys.argv[1], sys.argv[2] 


def main():
    constraintsFile, preferencesFile = parse_args()
    constraints_raw = open(constraintsFile, 'r').read().split('\n')
    constraints = Constraints(constraints_raw)
    preferences_raw = open(preferencesFile, 'r').read().split('\n')
    preferences = Preferences(preferences_raw)
    print (constraints)
    print (preferences)
    print (constraints.numTeach)
    





if __name__ == "__main__":
    main()