# put your routing program here
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
        third = int(individualline1[2])
        if individualline1[3] == '':
            fourth = 0
        else:
            fourth = int(individualline1[3])
        fifth = individualline1[4]
        road_segments.append([first, second, third, fourth, fifth])
