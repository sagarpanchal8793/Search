###put your routing program here
from operator import itemgetter

citygpsFilename = "city-gps.txt"
roadSegmentsFilename = "road-segments.txt"
city_gps = {}
visited_states=[]
road_segments = []

with open(citygpsFilename, 'r') as inputfile1:
    lines = [line.strip() for line in inputfile1]
    for line in lines:
        individualline = line.split()
        city_gps[individualline[0]] = [float(individualline[1]), float(individualline[2])]


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
        road_segments.append([first, second, third, fourth, fifth])


def successor(s):
    city_name=s[0]
    succ=[]
    # [connectedCityName, [Path till that connected city], total distance, total time, totalsegments, highwaynames, heuristicFunction]
    for r in range(0, len(road_segments)):
        if road_segments[r][0] == city_name:
            succ.append([road_segments[r][1], s[1]+[city_name], s[2]+road_segments[r][2], s[3]+float(road_segments[r][2]/road_segments[r][3]), s[4]+1, s[5]+[road_segments[r][4]]])
        elif road_segments[r][1] == city_name:
            succ.append([road_segments[r][0], s[1]+[city_name], s[2]+road_segments[r][2], s[3]+float(road_segments[r][2]/road_segments[r][3]), s[4]+1, s[5]+[road_segments[r][4]]])
        else:
            pass
    return succ

def SolveBFS(initial_state):
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

def SolveDFS(initial_state):
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

def UniformCostSearch(initial_state):
    fringe=[initial_state]
    while len(fringe)>0:
        fringe = sorted(fringe, key=itemgetter(2)) # Sort on distance
        popped_fringe=fringe.pop(0)
        if popped_fringe[0] not in visited_states:
            visited_states.append(popped_fringe[0])
            for s in successor(popped_fringe):
                if s[0] == goal_city:
                    return(s)
                fringe.append(s)
    return False


goal_city = 'Fairborn,_Ohio'

solution = SolveBFS(['Abbot_Village,_Maine',[], 0,0,0,[]])

print "You have reached and path is : ",solution[1] if solution else "Sorry, no solution is found :("
print "The count of cities is: ", len(solution[1])
print "solution length : {0}".format(len(solution[1]))
print "total distance : {0}".format(solution[2])
print "total time : {0}".format(solution[3])
print "total segments : {0}".format(solution[4])
print "total highways : {0}".format(solution[5])
