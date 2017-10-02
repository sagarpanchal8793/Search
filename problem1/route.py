#!/usr/bin/env python
# route.py : Solve Navigation problem!
# Ameya Angal, Angad Dhillon, Sagar Panchal

# Analysis:
# Abstraction:
#   State : State is a list with following elements:
#             index 0: SourceCityName
#             index 1: List that contains Path taken to reach the the city mentioned in the 0th index
#             index 2: Distance travelled to reach city/junction in context
#             index 3: Time required to reach city/junction in context
#             index 4: Segments (turns) required to reach city/junction in context
#             index 5: List containing highways taken to reach city/junction in context
#             index 6: cost c(s) function (distance, time, segments)to reach city/junction in context
#             index 7: f(s) = c(s)+h(s),for a city/junction in context (This is present only for A* search)
#   Goal: Goal city as string.
#   Initial State: State with default values for index 1-7 and source city at index 0
#   cost function:
#       a) Distance: Added previous travelled distance with the distance between two connected cities from road-segments.txt
#       b) Time: Added previous time required with the distance between two connected cities, time = distance/speed (info given in road-segments.txt)
#       c) Segments: Added 1 to previous travelled segments. Segment is when highway is changed.
#   Heuristic: calculated distance between source city and goal city using latitude and longitude information in the city-gps
#         Distance is calculated using Haversine formula. For the cites/junctions that don't have latitude and longitude, we have returned
#         0, as with this case the total heuristic will be weak but will never overestimate. This heuristic is not consistent.
#   Successor: List of states for cities that are connected to the city whose successor needs to be found.
#
#   Assumption: 1) We have ignored the road-segments which has zero/blank distance or zero/blank speed
#               2) Assumed top speed as 150mph for calculating heuristic for time
#               3) Assumed maximum segments between source city and destination city as 1000 for calculating heuristic for segments
#
#
# 1) AStar search is working best for each routing options. As number of states expanded by Astar is always less than BFS, DFS and Uniform Cost
#   for every case. Folowing are the some examples:
#   San_Jose,_California Miami,_Florida uniform distance - Nodes expanded- 5847
#   San_Jose,_California Miami,_Florida astar distance -Nodes expanded 2071
#   San_Jose,_California Miami,_Florida bfs distance -Nodes expanded 6383
#   San_Jose,_California Miami,_Florida dfs distance -Nodes expanded 3373 (Nodes expanded is less than UCS and BFS but output is not optimal)

# 2) For us, some instances of test data have same Astar and Uniform Cost Search running time. But for most of the cases(with relatively close start city and goal city) Astar takes less time as nodes expanded are very less
#  than any other routing algorithm. As for longer routes, time for computing heuristic increases, UCS and astar have comparable running time.
#  We have a weak heuristic for cities/junctions having no known latitude and longitude, which cause more nodes to expand than ideal. 
#
#  For example:
#   San_Jose,_California Miami,_Florida dfs distance - time taken 0.577949047089 sec
#   San_Jose,_California Miami,_Florida dfs distance - time taken 1.27012586594 sec
#   San_Jose,_California Miami,_Florida uniform distance - time taken 1.73963713646 sec (time required is greater but path is optimal)
#   San_Jose,_California Miami,_Florida astar distance  - time taken 1.76955795288 sec (time required equals time required for UCS as heuristic calculation is taking time)

# 3) Memory requirement for astar is less than any other routing algorithm, as number of nodes expanded in astar is very less than any other
# routing algorithm. Hence number of states for which the successor function runs is less and hence the running time and memory requirement is less.

# 4) For Distance cost function, our heuristic gives the distance between current city and the goal city using latitude and longitude. But for
# cities/junctions with unknown latitude and longitude, we assume heuristic as 0. In this way it will always underestimate the actual distance.
# Our heuristic is not consistent, hence we have used search algorithm 2. After reading Piazza question @151, we have kept track of closed states
# but when we encounter a state with lower f(s) than earlier visited city, we remove the previous inserted state as there is a possiblity for shortest route.
#  For time cost function: We have assumed that maximum speed is 150mph. We have divided heuristic value by 150 so as to calculate least possible
# time required between current city and goal city (this way it doesn't overestimate)
# For segments cost function: We have assumed that maximum seegments between source and destination are 1000. We have divided heuristic value by 1000 so as to calculate least possible
# segments required between current city and goal city (this way it doesn't overestimate)

# 5) We have used Haversine formula to calculate distance between known latitude and longitude for 2 cities, which always gives the least path.
# So this is admissible. For citites/junctions with unknown latitude and longitude we have heuristic value = 0, which always underestimates.
# Our heuristic is not consistent. But after reading Piazza question @151, we have kept track of closed states and removed a state from closed when a
# shorter route is found and hence we give opimal output.


# put your routing program here
from operator import itemgetter
from math import sin, cos, sqrt, atan2, radians
import time
import sys


visited_states=[]

# buildds the city gps dictionary
citygpsfilename = "city-gps.txt"
city_gps = {}
with open(citygpsfilename, 'r') as inputfile1:
    lines = [line.strip() for line in inputfile1]
    for line in lines:
        individualline = line.split()
        city_gps[individualline[0]] = [float(individualline[1]), float(individualline[2])]


roadSegmentsFilename = "road-segments.txt"
road_segments = {}
# builds the road_segment dictionary
with open(roadSegmentsFilename, 'r') as inputfile2:
    lines1 = [line1.strip() for line1 in inputfile2]
    for line1 in lines1:
        individualline1= line1.split(' ')
        first = individualline1[0]
        second = individualline1[1]
        if int(individualline1[2]) == 0:
            continue
        else:
            third = int(individualline1[2])
        if individualline1[3] == '' or int(individualline1[3]) == 0:
            continue
        else:
            fourth = int(individualline1[3])
        fifth = individualline1[4]
        if first not in road_segments:
            road_segments[first]=[[second, third, fourth, fifth]]
        else:
            road_segments[first].append([second, third, fourth, fifth])
        if second not in road_segments:
            road_segments[second]=[[first, third, fourth, fifth]]
        else:
            road_segments[second].append([first, third, fourth, fifth])

# referred the Haversine distance calculation formula from "https://stackoverflow.com/questions/27928/calculate-distance-between-two-latitude-longitude-points-haversine-formula"
# returns the distance in miles between cities based on latitude and longitude
def distance(sourcelatitude, sourcelongitude, destinatiolatitude, destinationlongtitude):
    r = 3959.99 # radius of earth in miles
    longitudeDist = destinationlongtitude - sourcelongitude
    latitudeDist = destinatiolatitude - sourcelatitude
    altitude = sin(latitudeDist / 2) ** 2 \
                + cos(sourcelatitude) \
                * cos(destinatiolatitude) \
                * sin(longitudeDist / 2) ** 2
    c = 2 * atan2(sqrt(altitude), sqrt(abs(1 - altitude)))
    return r * c

# returns the heuristic value for a city, 0 if unknown latitude and longitudes
def Heuristicvalue(sourceCity):
    if goal_city in city_gps:
        destinationCityLatitude = radians(city_gps[goal_city][0])
        destinationCityLongitude = radians(city_gps[goal_city][1])
    else:
        return 0 # Set heuristic(for that city/junction) to 0 if latitude and longitude are not known - always underestimates

    if sourceCity in city_gps:
        sourceCityLatitude = radians(city_gps[sourceCity][0])
        sourceCityLongitude = radians(city_gps[sourceCity][1])
    else:
        return 0 # Set heuristic(for that city/junction) to 0 if latitude and longitude are not known - always underestimates

    return distance(sourceCityLatitude, sourceCityLongitude, destinationCityLatitude, destinationCityLongitude)

# returns successors for uniform cost search/ bfs/ dfs for a particular state
def successor(s, cost = " "):
    city_name = s[0]
    # State = [connectedCityName, [Path till that connected city], total distance, total time, totalsegments, highwaynames, c(s)]
    # For distance c(s) is distance till this state
    if cost == "distance":
        return [[values[0], s[1] + [city_name], s[2] + values[1], s[3] + float(values[1]) / float(values[2]), s[4] + 1,
                    s[5] + [values[3]], s[2] + values[1]] \
                for values in road_segments[city_name]]
    # For time c(s) is distance/speed till this state
    elif cost == "time":
        return [[values[0], s[1] + [city_name], s[2] + values[1], s[3] + float(values[1]) / float(values[2]), s[4] + 1,
                    s[5] + [values[3]], s[3] + float(values[1]) / float(values[2])] \
                for values in road_segments[city_name]]
    # For segments c(s) is number of segments (highway changed) till this state
    elif cost == "segments":
        return [[values[0], s[1] + [city_name], s[2] + values[1], s[3] + float(values[1]) / float(values[2]), s[4] + 1,
                    s[5] + [values[3]], s[4] + 1] \
                for values in road_segments[city_name]]
    else:
        return [[values[0], s[1] + [city_name], s[2] + values[1], s[3] + float(values[1]) / float(values[2]), s[4] + 1,
                 s[5] + [values[3]]] \
                for values in road_segments[city_name]]

# returns successors for astar search for a particular state
def AStarsuccessor(s, cost = " "):
    city_name = s[0]
    # State = [connectedCityName, [Path till that connected city], total distance, total time, totalsegments, highwaynames, c(s), f(s)]
    # For distance f(s) is distance (till this state) + heuristicvalue(currentcity)
    if cost == "distance":
        return [[values[0], s[1] + [city_name], s[2] + values[1], s[3] + float(values[1]) / float(values[2]), s[4] + 1,
                    s[5] + [values[3]], s[2] + values[1], s[2]+values[1]+ Heuristicvalue(values[0])] \
                for values in road_segments[city_name]]
    # For time f(s) is time (till this state) + heuristicvalue(currentcity) / 150 (divided by maximum poossible speed)
    elif cost == "time":
        return [[values[0], s[1] + [city_name], s[2] + values[1], s[3] + float(values[1]) / float(values[2]), s[4] + 1,
                    s[5] + [values[3]], s[3] + float(values[1])/float(values[2]), s[3] + float(values[1])/float(values[2]) + Heuristicvalue(values[0])/150.0] \
                for values in road_segments[city_name]]
    # For segments f(s) is segments (till this state) + heuristicvalue(currentcity) / 1000 (divided by maximum poossible segments in longest route)
    elif cost == "segments":
        return [[values[0], s[1] + [city_name], s[2] + values[1], s[3] + float(values[1]) / float(values[2]), s[4] + 1,
                    s[5] + [values[3]], s[4] + 1, s[4] + 1 + (Heuristicvalue(values[0])/1000.0)] \
                for values in road_segments[city_name]]
    else:
        return [[values[0], s[1] + [city_name], s[2] + values[1], s[3] + float(values[1]) / float(values[2]), s[4] + 1,
                 s[5] + [values[3]], s[2] + values[1], s[2]+values[1]+ Heuristicvalue(values[0])] \
                for values in road_segments[city_name]]


# solve using bfs algorithm
def SolveBFS(initial_state, cost = ""):
    statecount = 0
    fringe=[initial_state]
    while len(fringe)>0:
        popped_fringe=fringe.pop(0)
        if popped_fringe[0] not in visited_states:
            statecount +=1
            visited_states.append(popped_fringe[0])
            for s in successor(popped_fringe):
                if s[0] == goal_city:
                    return(s)
                fringe.append(s)
    return False

# solve using dfs algorithm
def SolveDFS(initial_state, cost = ""):
    fringe=[initial_state]
    statecount = 0
    while len(fringe)>0:
        popped_fringe=fringe.pop()
        if popped_fringe[0] not in visited_states:
            statecount +=1
            visited_states.append(popped_fringe[0])
            for s in successor(popped_fringe):
                if s[0] == goal_city:
                    return(s)
                fringe.append(s)
    return False

# solve using uniform cost search algorithm
def UniformCostSearch(initial_state, cost):
    statecount = 0
    if initial_state[0] == goal_city:
        return initial_state
    fringe=[initial_state]
    while len(fringe)>0:
        fringe = sorted(fringe, key=itemgetter(6)) # Sort on c(s)
        popped_fringe=fringe.pop(0)
        if popped_fringe[0] == goal_city:
            return(popped_fringe)
        if popped_fringe[0] not in visited_states:
            statecount += 1
            visited_states.append(popped_fringe[0])
            for s in successor(popped_fringe, cost):
                fringe.append(s)
    return False

# referred question @151 on Piazza and removed a state (higher cost) present in closed, as my heuristic function is not consistent
# removes a state from closed list if current state has a lower f(s) value (as)
def removeStateIfInClosedWithHigherHeuristic(state, closed):
    for item in closed:
        if item[0] == state[0] and item[7] > state[7]:
            closed.remove(item)

# checks if a state is present in closed
def IsStateInClosed(state, closed):
    for element in closed:
        if element[0] == state[0]:
            return True
    return False

# solve using a star algorithm
def solve_astar(initial_state, cost):
    statecount = 0
    if initial_state[0] == goal_city:
        return initial_state
    fringe = [initial_state]
    closed = []
    while len(fringe) > 0:
        fringe = sorted(fringe, key=itemgetter(7)) # Sort on f(s)
        popped_fringe = fringe.pop(0)
        if popped_fringe[0] == goal_city:
            return popped_fringe
        # if popped in closed, continue else closed append and expand
        if not IsStateInClosed(popped_fringe, closed):
            closed.append(popped_fringe)
            statecount += 1
            for s in AStarsuccessor(popped_fringe, cost):
                removeStateIfInClosedWithHigherHeuristic(s, closed)
                fringe.append(s)
    return False

def printRoute(solution):
    if len(solution[1]) == 0:
        print "{0} {1} {2} {3}".format(solution[2], solution[3], start_city, goal_city)
    else:
        for i in range(0, len(solution[1])-1):
            connectedhighway = ""
            dist = 0
            for connectedcity in road_segments[solution[1][i]]:
                if connectedcity[0] == solution[1][i+1]:
                    connectedhighway = connectedcity[3]
                    dist = connectedcity[1]
            print "From {0} to {1} via highway {2} for {3} miles ".format(solution[1][i], solution[1][i+1], connectedhighway, dist)
        print "{0} {1} {2} {3}".format(solution[2], solution[3], " ".join([str(x) for x in solution[1]]), goal_city)


def IsCityValid(cityname):
    return cityname in road_segments


def IsCostFunctionValid(routing_algorithm):
    return routing_algorithm in ["segments", "distance", "time"]


def IsRoutingAlgorithmValid(costfunction):
    return costfunction in ["bfs","uniform","dfs","astar"]


def IsInputvalid():
    if not IsCityValid(goal_city) or not IsCityValid(start_city):
        print "Invalid start city or goal city"
        return False
    if not IsRoutingAlgorithmValid(routing_algorithm):
        print "Invalid routing algorithm"
        return False
    if not IsCostFunctionValid(costfunction):
        print "Invalid cost function"
        return False
    # if routing_algorithm == "uniform" or routing_algorithm == "astar":
        # global costfunction
        # costfunction = sys.argv[4]
    return True


start_city = sys.argv[1]
goal_city = sys.argv[2]
routing_algorithm = sys.argv[3]
costfunction = sys.argv[4]

if IsInputvalid():
    initial_state = [start_city, [], 0, 0, 0,[], 0, Heuristicvalue(start_city)]
    if routing_algorithm == "bfs":
        solution = SolveBFS(initial_state)
    elif routing_algorithm == "uniform":
        solution = UniformCostSearch(initial_state, costfunction)
    elif routing_algorithm == "dfs":
        solution = SolveDFS(initial_state)
    else:
        solution = solve_astar(initial_state, costfunction)
    printRoute(solution)
else:
    print "Invalid Input"
