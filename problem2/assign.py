# put your group assignment problem here!
# !/usr/bin/env python3

#!/usr/bin/env python3

# (1) A description of how you formulated the search problem, including precisely defining the state space, the successor function,
# the edge weights, the goal state, and (if applicable) the heuristic function(s) you designed, including an argument 
# for why they are admissible.

# Ans:

# 1. State space:
#       It consists of all the possible states starting from the initial state which is a blank list of groups that will be
# used to generate the successor. The states generated from the initial state will not contain more than 3 students per group and
# also the number of groups cannot be more than the number of distinct students.

# 2. Successor Function:
#       It generates new states from the current state by simply adding a new student in a list of groups i.e.
# If we have 6 students then the successor function will create 6 list of groups which will contain those 6 students resepectively in
# each list. In the next iteration a new student will be added either adjacently to the student who is already present or as a new
# member of the next group. Similarly, successors will be created for all the states.

# 3. Edge weights:
#       The edge weights for this question (according to us) is the cost per list of groups (basically successors) that is being
# caluclated based on the team size(1 min), preference(n) and non preference(m) of the students as well as the grading time(k) that will be required
# for each group in the list. (Suppose we have 5 groups so we will add 5*k into the final cost i.e. the time required by the staff to
# evaluate each assignment)

# 4. Goal State:
#       As per our understanding we think that we do not have a single goal state for this question. As we have to find the most
# optimal solution that should be the least amount of time staff has the invest to evaluate the assignment keeping in mind that
# groups must contain all the distinct students and no student should be assigned more than once.

# (2) A brief description of how your search algorithm works.

# Ans:
#       Our first approach was to find the optimal solution based on the cost of the successors generated. In this approach we used a
# fringe from which we selected the minimum cost state and generated successors for that state now we put this successors back in the
# fringe and again select the least cost state for which successors are generated and this continuous till we reach our goal state. In
# this algorithm we have defined goal state as the minimum cost option out of a set of goal states(states containing all distinct users
# in them). The execution time required for generating the optimal solution using this algorithm was exponential after the number of
# students (those who have filled the survey details) goes beyond 6. So to find a solution in a reasonable execution time for this
# assignment we have also used Steepest Descent algorithm which gives a less optimal solution but in very less time as compared to the
# previous one.

# (3) Discussion of any problems you faced, any assumptions, simplifications, and/or design decisions you made.

# Ans:
#       We have added an "If-else" condition at the end of the code where we actually call the solution function, this condition checks
# the number of students who have filled the survey  are lesser than 7 or greater than equal to 7 and based on this conditions our 2
# different algorithms will be called respectively. The reason for doing this is that for input less than 6 the algorithm works fast
# and gives us the optimal solution as per the design but when the input size increases the time taken to find the solution increases
# exponentially. Hence, to overcome this issue we designed another function using Steepest Descent algorithm which gives us very fast
# output even for large input sizes. The only problem with steepest descent is that we do not know whether the end result given by the
# algorithm is optimal or not.

import sys
import copy
from operator import itemgetter

survey_details = {}
fringe = []

# Command line arguments
inputFilename = sys.argv[1]
k = int(sys.argv[2])
m = int(sys.argv[3])
n = int(sys.argv[4])

#Generated a dictionary of the input file for the optimum retreival of data when required.
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

# This list is generated to use it for generating the successors.        
user_list = [user_id for user_id, values in survey_details.items()]

# This function will generate the successors of the current state given to it.
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

# This is the Cost function which will generate the heuristic value of the successors that are being passed to it.
# Heuristic value is being calculated on the basis of the k, m & n values that are given through the command line parameters.
# So each and every student's team size preference, student preferred list and non preferred list is evaluated to get the final cost
# of creating those groups and that entire cost is stored in the list which contains the groups.
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

# This function is used to check whether we have made the teams with the least cost and check whether all the users are present in
# any one of the group or not. Also we have created 2 solution functions performing the same thing except for the number of students
# giving the survey.

# Solution #1 (below mentioned function) will be used when the number of students is greater than or equal to 7 which gives us non optimal solution
# but in very less time as compared to the other one.
# Max input we gave is for 100 students and the output took us almost 2m 37s
def solution(successors_returned):
    fringe_solutions_list = []
    user_list2 = copy.deepcopy(user_list)
    fringe = []
    for p in range(0, len(successors_returned)):
        fringe.append(successors_returned[p])
    while len(fringe) > 0:
        # https://stackoverflow.com/questions/4690416/sorting-dictionary-using-operator-itemgetter?lq=1
        fringe = sorted(fringe, key=itemgetter(1))
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

# Solution #2 (below mentioned function) will be used when the number of students are less than 7 which gives us the optimal
# solution (according to us) but executes comparatively slow than the previous one.
# It runs very well for the sample input given to us in the assignment file itself.
def solution_optimized(successors_returned):
    fringe_solutions_list = []
    user_list2 = copy.deepcopy(user_list)
    fringe = []
    for p in range(0, len(successors_returned)):
        fringe.append(successors_returned[p])
    while len(fringe) > 0:
        # https://stackoverflow.com/questions/4690416/sorting-dictionary-using-operator-itemgetter?lq=1
        fringe = sorted(fringe, key=itemgetter(1))
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

# Saving the length of the data retreived from the input file so as to generate the intial state
N = len(user_list)

# Initial state is generated which is an empty list of list(inner list will contain the list of groups of students) with cost value as 0
list_passing = [[[] for i in range(N)], 0]
output = []

# Condition to check if count of students in input file (which contains records of survey details) is lesser than 7
if len(user_list) < 7:
    output = solution_optimized(cost_function(succ(list_passing)))
# else if count is greater than or equal to 7     
elif len(user_list) >= 7:
    output = solution(cost_function(succ(list_passing)))

# Code to format the result as required    
for r in output[0]:
    if len(r) > 0:
        print(' '.join(r))
print(output[1])
