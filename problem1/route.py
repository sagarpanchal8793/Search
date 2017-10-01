# put your routing program here
from operator import itemgetter
from math import sin, cos, sqrt, atan2, radians

import time

import sys

citygpsfilename = "city-gps.txt"
visited_states=[]

# bukds the city gps dictionary
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

# returns the distance between cities based on latitude and longitude
def distance(sourcelatitude, sourcelongitude, destinatiolatitude, destinationlongtitude):
    r = 3959.99
    longitudeDist = destinationlongtitude - sourcelongitude
    latitudeDist = destinationlongtitude - sourcelatitude
    altitude = sin(latitudeDist / 2) ** 2 \
                + cos(sourcelatitude) \
                * cos(destinatiolatitude) \
                * sin(longitudeDist / 2) ** 2
    c = 2 * atan2(sqrt(altitude), sqrt(abs(1 - altitude)))
    return r * c

# returns the cartesian cordinates for a particular city whose lat and long are unknown
def calculatecartesianCoordinates(city, depth, connectedDone):
    connectedcities = [value[0] for value in road_segments[city]]
    x = 0
    y = 0
    z = 0
    length = 0
    if depth < 3:
        for connectedcity in connectedcities:
            if connectedcity not in connectedDone:
                if connectedcity in city_gps:
                    connectedDone.append(connectedcity)
                    length += 1
                    lat = radians(city_gps[connectedcity][0])
                    lon = radians(city_gps[connectedcity][1])
                    x += cos(lat) * cos(lon)
                    y += cos(lat) * sin(lon)
                    z += sin(lat)
                else:
                    if depth != 2: # ignore junctions for level 2
                        connectedDone.append(connectedcity)
                        x1, y1, z1 = calculatecartesianCoordinates(connectedcity, depth+1, connectedDone)
                        if x!=0 and y!=0 and z!=0:
                            length += 1
                        x += x1
                        y += y1
                        z += z1
        if length == 1:
            length = 2 # default lenght if connected to only one city
        if length == 0:
            return 0,0,0
        return x/length, y/length, z/length
    else:
        return 0, 0, 0

# returns the latitude and longitude for a city whose lat and long are unknown
def calculateLatitudeAndLongitude(city):
    X, Y, Z = calculatecartesianCoordinates(city, 0, [city])
    longitude = atan2(Y, X)
    hyp = sqrt(X*X + Y*Y)
    latitude = atan2(Z, hyp)
    return latitude, longitude

# returns the heuristic value for a city
def Heuristicvalue(sourceCity):
    if goal_city in city_gps:
        destinationCityLatitude = radians(city_gps[goal_city][0])
        destinationCityLongitude = radians(city_gps[goal_city][1])
    else:
        destinationCityLatitude, destinationCityLongitude = calculateLatitudeAndLongitude(goal_city)

    if sourceCity in city_gps:
        sourceCityLatitude = radians(city_gps[sourceCity][0])
        sourceCityLongitude = radians(city_gps[sourceCity][1])
    else:
        sourceCityLatitude, sourceCityLongitude = calculateLatitudeAndLongitude(sourceCity)

    return distance(sourceCityLatitude, sourceCityLongitude, destinationCityLatitude, destinationCityLongitude)

# returns successors for uniform cost search for a particular state
def successor(s, cost = " "):
    city_name = s[0]
    # [connectedCityName, [Path till that connected city], total distance, total time, totalsegments, highwaynames, c(s)]
    if cost == "distance":
        return [[values[0], s[1] + [city_name], s[2] + values[1], s[3] + float(values[1]) / float(values[2]), s[4] + 1,
                    s[5] + [values[3]], s[2] + values[1]] \
                for values in road_segments[city_name]]
    elif cost == "time":
        return [[values[0], s[1] + [city_name], s[2] + values[1], s[3] + float(values[1]) / float(values[2]), s[4] + 1,
                    s[5] + [values[3]], s[3] + float(values[1]) / float(values[2])] \
                for values in road_segments[city_name]]
    elif cost == "segments":
        return [[values[0], s[1] + [city_name], s[2] + values[1], s[3] + float(values[1]) / float(values[2]), s[4] + 1,
                    s[5] + [values[3]], s[4] + 1] \
                for values in road_segments[city_name]]
    else:
        return [[values[0], s[1] + [city_name], s[2] + values[1], s[3] + float(values[1]) / float(values[2]), s[4] + 1,
                 s[5] + [values[3]]] \
                for values in road_segments[city_name]]
    # return [[values[0], s[1] + [city_name], s[2] + values[1], s[3] + float(values[1]) / float(values[2]), s[4] + 1,
    #          s[5] + [values[3]], s[2]+values[1]+ Heuristicvalue(values[0])] for values in road_segments[city_name]]

def AStarsuccessor(s, cost = " "):
    city_name = s[0]
    # [connectedCityName, [Path till that connected city], total distance, total time, totalsegments, highwaynames, c(s), f(s)]
    if cost == "distance":
        return [[values[0], s[1] + [city_name], s[2] + values[1], s[3] + float(values[1]) / float(values[2]), s[4] + 1,
                    s[5] + [values[3]], s[2] + values[1], s[2]+values[1]+ Heuristicvalue(values[0])] \
                for values in road_segments[city_name]]
    elif cost == "time":
        return [[values[0], s[1] + [city_name], s[2] + values[1], s[3] + float(values[1]) / float(values[2]), s[4] + 1,
                    s[5] + [values[3]], s[3] + float(values[1])/float(values[2]), s[3] + float(values[1])/float(values[2]) + Heuristicvalue(values[0])/65.0] \
                for values in road_segments[city_name]]
    elif cost == "segments":
        return [[values[0], s[1] + [city_name], s[2] + values[1], s[3] + float(values[1]) / float(values[2]), s[4] + 1,
                    s[5] + [values[3]], s[4] + 1, s[4] + 1 + Heuristicvalue(values[0])/500] \
                for values in road_segments[city_name]]
    else:
        return [[values[0], s[1] + [city_name], s[2] + values[1], s[3] + float(values[1]) / float(values[2]), s[4] + 1,
                 s[5] + [values[3]], s[2] + values[1], s[2]+values[1]+ Heuristicvalue(values[0])] \
                for values in road_segments[city_name]]


# solve bfs algorithm
def SolveBFS(initial_state, cost = ""):
    fringe=[initial_state]
    while len(fringe)>0:
        popped_fringe=fringe.pop(0)
        if popped_fringe[0] not in visited_states:
            visited_states.append(popped_fringe[0])
            for s in successor(popped_fringe):
                if s[0] == goal_city:
                    return(s)
                fringe.append(s)
    return False

# solve using dfs algorithm
def SolveDFS(initial_state, cost = ""):
    fringe=[initial_state]
    while len(fringe)>0:
        popped_fringe=fringe.pop()
        if popped_fringe[0] not in visited_states:
            visited_states.append(popped_fringe[0])
            for s in successor(popped_fringe):
                if s[0] == goal_city:
                    return(s)
                fringe.append(s)
    return False

# solve using uniform cost search algorithm
def UniformCostSearch(initial_state, cost):
    fringe=[initial_state]
    while len(fringe)>0:
        fringe = sorted(fringe, key=itemgetter(6))
        popped_fringe=fringe.pop(0)
        if popped_fringe[0] == goal_city:
            return(popped_fringe)
        if popped_fringe[0] not in visited_states:
            visited_states.append(popped_fringe[0])
            for s in successor(popped_fringe, cost):
                fringe.append(s)
    return False

# removes a state from closed list if state has a higher heuristic
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
    if initial_state[0] == goal_city:
        return initial_state
    fringe = [initial_state]
    closed = []
    while len(fringe) > 0:
        fringe = sorted(fringe, key=itemgetter(7))
        popped_fringe = fringe.pop(0)
        # if popped in closed, continue else closed append and expand
        if not IsStateInClosed(popped_fringe, closed):
            closed.append(popped_fringe)
            if popped_fringe[0] == goal_city:
                return popped_fringe
            else:
                for s in AStarsuccessor(popped_fringe, cost):
                    removeStateIfInClosedWithHigherHeuristic(s, closed)
                    fringe.append(s)
    return False

def printRoute(route):
    for i in range(0, len(route)-1):
        connectedhighway = ""
        dist = 0
        for connectedcity in road_segments[route[i]]:
            if connectedcity[0] == route[i+1]:
                connectedhighway = connectedcity[3]
                dist = connectedcity[1]
        print "From {0} to {1} via highway {2} for {3} miles".format(route[i], route[i+1], connectedhighway, dist)


def IsCityValid(cityname):
    return cityname in road_segments


def IsCostFunctionValid(routing_algorithm):
    return routing_algorithm in ["segments", "distance", "time"]

def IsRoutingAlgorithmValid(costfunction):
    return costfunction in ["bfs","uniform","dfs","astar"]

def IsInputvalid():
    # valid = True
    if not IsCityValid(goal_city) or not IsCityValid(start_city):
        return False
    if not IsRoutingAlgorithmValid(routing_algorithm):
        return False
    if routing_algorithm == "uniform" or routing_algorithm == "astar":
        global costfunction
        # costfunction = sys.argv[4]
    return True
    #
    # return  \
    #        and IsCityValid(start_city) \
    #        and IsRoutingAlgorithmValid(routing_algorithm) \
    #        and IsCostFunctionValid(costfunction)


start_city = sys.argv[1]
goal_city = sys.argv[2]
routing_algorithm = sys.argv[3]
costfunction = sys.argv[4]

if IsInputvalid():
    initial_state = [start_city, [], 0, 0, 0,[], 0, Heuristicvalue(start_city)]

    start = time.time()
    if routing_algorithm == "bfs":
        solution = SolveBFS(initial_state)
    elif routing_algorithm == "uniform":
        solution = UniformCostSearch(initial_state, costfunction)
    elif routing_algorithm == "dfs":
        solution = SolveDFS(initial_state)
    else:
        solution = solve_astar(initial_state, costfunction)

    printRoute(solution[1])
    end = time.time()
    print "{0} {1} {2} {3}".format(solution[2], solution[3], " ".join([str(x) for x in solution[1]]), goal_city)
else:
    print "Invalid Input"


# goal_city = 'Abbot_Village,_Maine'
# goal_city = 'Dallas,_Texas'

# goal_city = 'Los_Angeles,_California'
# initial_state = ['Virginia_Colony,_California', [], 0, 0, 0,[], Heuristicvalue('Virginia_Colony,_California')]

# solution = solve_astar(initial_state, "distance")

# print("You have reached and path is: {0}".format(solution[1]) if solution else "Sorry, no solution is found :(")
# print "solution length : {0}".format(len(solution[1]))
# print "total distance : {0}".format(solution[2])
# print "total time : {0}".format(solution[3])
# # print "total segments : {0}".format(solution[4])
# print "total highways : {0}".format(solution[4])
# print "time taken : {0}".format(end-start)

# start = time.time()
# print "AStar"
# solution1 = solve_astar(initial_state)
# end = time.time()
#
# print("You have reached and path is: {0}".format(solution1[1]) if solution1 else "Sorry, no solution is found :(")
# print "solution length : {0}".format(len(solution1[1]))
# print "total distance : {0}".format(solution1[2])
# print "total time : {0}".format(solution1[3])
# print "total segments : {0}".format(solution1[4])
# print "total highways : {0}".format(solution1[5])
# print "time taken : {0}".format(end-start)

# print "distnace {0}".format(Heuristicvalue('Lakes_District,_Washington'))