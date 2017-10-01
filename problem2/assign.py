# put your group assignment problem here!
# !/usr/bin/env python3
import sys
import copy
from operator import itemgetter

survey_details = {}
fringe = []
inputFilename = sys.argv[1]
k = int(sys.argv[2])
m = int(sys.argv[3])
n = int(sys.argv[4])

with open(inputFilename, 'r') as inputfile1:
    lines = [line.strip() for line in inputfile1]
    for line in lines:
        pref_list = []
        non_pref_list = []

        individualline = line.split(' ')
        user_id = individualline[0]
        team_size = individualline[1]

        pref = individualline[2].split(',')
        for item in pref:
            pref_list.append(item)

        non_pref = individualline[3].split(',')
        for item in non_pref:
            non_pref_list.append(item)

        survey_details[user_id] = [int(team_size), pref_list, non_pref_list]
user_list = [user_id for user_id, values in survey_details.items()]


def succ(teams_made):
    user_list1 = copy.deepcopy(user_list)
    temp_list = []
    successors_list = []
    for j in range(0, len(teams_made[0])):
        for i in range(0, len(teams_made[0][j])):
            temp_list.append(teams_made[0][j][i])
    for t in temp_list:
        user_list1.remove(t)

    successors = []
    for y in range(0, len(user_list1)):
        for z in range(0, len(teams_made[0])):
            teams_made1 = copy.deepcopy(teams_made)
            if (z == 0) and (len(teams_made1[0][z]) < 3):
                teams_made1[0][z].append(user_list1[y])
                successors.append(teams_made1)
            elif z > 0 and (len(teams_made1[0][z]) < 3):
                if (len(teams_made1[0][z - 1]) != 0):
                    teams_made1[0][z].append(user_list1[y])
                    successors.append(teams_made1)
    return successors


def cost_function(successors):
    len_successors = len(successors)
    for r in range(0, len_successors):
        team_cost = 0
        number_teams = 0
        for j in range(0, len(successors[r][0])):

            size_cost = 0
            number_emails = 0
            number_meetings = 0
            if len(successors[r][0][j]) != 0:
                number_teams = number_teams + 1
            for y in range(0, len(successors[r][0][j])):
                preference_list = []
                preference_list = survey_details[successors[r][0][j][y]]
                team_size = preference_list[0]
                team_preference = preference_list[1]
                team_not_preferred = preference_list[2]
                if team_size != 0 and team_size != len(successors[r][0][j]):
                    size_cost = size_cost + 1
                elif team_size == 0:
                    size_cost = size_cost + 0
                for l in team_preference:
                    if l not in successors[r][0][j]:
                        number_emails = number_emails + 1

                for z in team_not_preferred:
                    if z in successors[r][0][j]:
                        number_meetings = number_meetings + 1
                team_cost = team_cost + (size_cost) + (n * number_emails) + (m * number_meetings)

        successors[r][1] = team_cost + k * number_teams

    return successors


def solution(successors_returned):
    fringe_solutions_list = []
    user_list2 = copy.deepcopy(user_list)
    fringe = []
    for p in range(0, len(successors_returned)):
        fringe.append(successors_returned[p])
    # print(fringe)
    while len(fringe) > 0:
        fringe = sorted(fringe, key=itemgetter(
            1))  # https://stackoverflow.com/questions/4690416/sorting-dictionary-using-operator-itemgetter?lq=1
        successors_returned1 = cost_function(succ(fringe.pop(0)))
        fringe = []
        for p in range(0, len(successors_returned1)):
            fringe.append(successors_returned1[p])
        for j in range(0, len(fringe)):
            temp_list = []
            count = 0
            for i in range(0, len(fringe[j][0])):
                for q in range(0, len(fringe[j][0][i])):
                    temp_list.append(fringe[j][0][i][q])
            for t in temp_list:
                if t in user_list2:
                    count += 1
            if count == len(user_list2):
                return (fringe[j])


def solution_optimized(successors_returned):
    fringe_solutions_list = []
    user_list2 = copy.deepcopy(user_list)
    fringe = []
    for p in range(0, len(successors_returned)):
        fringe.append(successors_returned[p])
    while len(fringe) > 0:
        fringe = sorted(fringe, key=itemgetter(
            1))  # https://stackoverflow.com/questions/4690416/sorting-dictionary-using-operator-itemgetter?lq=1
        successors_returned1 = cost_function(succ(fringe.pop(0)))
        for p in range(0, len(successors_returned1)):
            fringe.append(successors_returned1[p])
        for j in range(0, len(fringe)):
            temp_list = []
            count = 0
            for i in range(0, len(fringe[j][0])):
                for q in range(0, len(fringe[j][0][i])):
                    temp_list.append(fringe[j][0][i][q])
            for t in temp_list:
                if t in user_list2:
                    count += 1
            if count == len(user_list2):
                fringe_solutions_list.append(fringe[j])
                if (len(fringe_solutions_list) == len(user_list)):
                    fringe_solutions_list = sorted(fringe_solutions_list, key=itemgetter(1))
                    return (fringe_solutions_list[0])


N = len(user_list)

list_passing = [[[] for i in range(N)], 1]
output = []
if len(user_list) < 7:
    output = solution_optimized(cost_function(succ(list_passing)))
elif len(user_list) >= 7:
    output = solution(cost_function(succ(list_passing)))
for r in output[0]:
    if len(r) > 0:
        print(' '.join(r))
print(output[1])
