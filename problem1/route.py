# put your routing program here

filename = "city-gps.txt"
city_gps = []
visited_states=[]
goal_city = 'Jackman_Station,_Maine'

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
        third = int(individualline1[2])
        if individualline1[3] == '':
            fourth = 0
        else:
            fourth = int(individualline1[3])
        fifth = individualline1[4]
        road_segments.append([first, second, third, fourth, fifth])


def successor(s):
    city_name=s
    succ=[]
    for r in range(0,len(road_segments)):      
            if road_segments[r][0]==city_name:
                succ.append(road_segments[r][1])
                
            elif road_segments[r][1] == city_name:
                succ.append(road_segments[r][0])
    return (succ)

def solve_using_dfs(start_city):
    fringe=[start_city]
    
    while len(fringe)>0:
        popped_fringe=fringe.pop()
        print("Popped Fringe is: ")
        print(popped_fringe)
        if popped_fringe not in visited_states:
            visited_states.append(popped_fringe)
            print ("Visited states are as follows: ")
            print(visited_states)
            for s in successor(popped_fringe):
                if s == goal_city:
                    return(s)
                fringe.append(s)
    return False
    
            
    
solution = solve_using_dfs('Abbot_Village,_Maine')
print("You have reached: "+solution if solution else "Sorry, no solution is found :(")
    
    