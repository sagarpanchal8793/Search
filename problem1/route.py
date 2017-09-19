###put your routing program here

filename = "city-gps.txt"
city_gps = []


with open(filename, 'r') as inputfile1:
    lines = [line.strip() for line in inputfile1]
    for line in lines:
        individualline = line.split()
        first = individualline[0]
        second = float(individualline[1])
        third = float(individualline[2])
        city_gps.append([first, second, third])


filename = "road-segments.txt"
road_segments = []
with open(filename, 'r') as inputfile2:
    lines1 = [line1.strip() for line1 in inputfile2]
    for line1 in lines1:
        individualline1= line1.split(' ')
        first = individualline1[0]
        second = individualline1[1]
        if individualline1[2] == 0:
            continue
        else:
            third = int(individualline1[2])
        if individualline1[3] == '' or individualline1[3] == 0:
            continue
        else:
            fourth = int(individualline1[3])  
        fifth = individualline1[4]
        road_segments.append([first, second, third, fourth, fifth])


def successor(s):
    city_name=s[0]
    succ=[]
    
    for r in range(0,len(road_segments)):
        if road_segments[r][0] == city_name:
            succ.append([road_segments[r][1],s[1]+[city_name]])
                
        elif road_segments[r][1] == city_name:
            succ.append([road_segments[r][0],s[1]+[city_name]])
            
    return (succ)

visited_states=[]

def solve_using_bfs(initial_state):
    fringe=[initial_state]
    
    while len(fringe)>0:
        popped_fringe=fringe.pop(0)
        if popped_fringe[0] not in visited_states:
            visited_states.append(popped_fringe[0])
            for s in successor(popped_fringe):
                if len(s)>0:
                    if s[0] == goal_city:
                        return(s)
                    fringe.append(s)
    return False

def solve_using_dfs(initial_state):
    fringe=[initial_state]
    
    while len(fringe)>0:
        popped_fringe=fringe.pop()
        if popped_fringe[0] not in visited_states:
            visited_states.append(popped_fringe[0])
            for s in successor(popped_fringe):
                if len(s)>0:
                    if s[0] == goal_city:
                        return(s)
                    fringe.append(s)
                    
    return False
    

goal_city = 'Fairborn,_Ohio'
        
solution = solve_using_bfs(['Abbot_Village,_Maine',[]])

print "You have reached and path is : ",solution[1] if solution else "Sorry, no solution is found :("
print "The count of cities is: ", len(solution[1])
