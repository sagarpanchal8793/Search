# put your 15 puzzle solver here!
from operator import itemgetter
import copy
import math
# State: [[[],[],[],[]], [moves to get to that state], c(s),f(s)]

# initial_state = [[[5,1,2,3],[0,9,6,4],[13,10,7,11],[14,15,12,8]],[], 0, 0] # 8 steps
initial_state = [[[2,1,3,4],[5,6,7,8],[9,10,0,12],[13,14,11,15]],[], 0, 0] # not working apprx 9 steps
# initial_state = [[[1,2,7,3],[5,10,6,4],[9,11,15,8],[13,14,0,12]],[], 0, 0]
# initial_state = [[[1,3,6,4],[5,11,2,8],[0,9,7,12],[13,10,14,15]],[], 0, 0]
goal_state = [[[1,2,3,4],[5,6,7,8],[9,10,11,12],[13,14,15,0]],[]]
# fringe = [initial_state]
# currentState = [[[1,2,3,4],[5,6,7,8],[9,10,0,12],[13,14,15,11]],[], 0, 9]
goalStatePositions = {}

def CreateGoalStatePositionsDictionary(goal):
    for i, row in enumerate(goal):
        for j, col in enumerate(row):
            goalStatePositions[goal[i][j]] = [i,j]


def GenerateParity(state):
    parityInversion = 0
    i = 0
    j = 0
    flat_list = [item for element in state for item in element]
    for i in range(0, len(flat_list)):
        for j in range(i+1, len(flat_list)):
            if flat_list[j] == 0 or flat_list[i] == 0:
                continue
            if flat_list[j]<flat_list[i]:
                parityInversion = parityInversion + 1
    return parityInversion
    # parityInversion = parityInversion + 1 for i in range(0, len(flat_list)) for j in range(i+1, len(flat_list)) if flat_list[j]<flat_list[i]

def IsParityInversionSatisfied(currentstate, goal_state):
    goalParity = GenerateParity(goal_state)
    stateparity = GenerateParity(currentstate)
    return (goalParity % 2) == (stateparity % 2)

#  returns a position of blank tile in the given puzzle
def FindPositionOfBlankTile(puzzle):
    return [(row, col) for row in range(0, 4) for col in range(0, 4) if puzzle[row][col] == 0]

# returns the manhattan distance for the puzzle state
def ManhattanDistance(puzzle):
    manhattanDistance = 0
    for i, row in enumerate(puzzle):
        for j, col in enumerate(row):
            if col == 0:
                continue
            manhattanDistance = manhattanDistance + abs(goalStatePositions[col][0] - i) + abs(goalStatePositions[col][1] - j)
    return  manhattanDistance

# return heuristic value MD/3
def heuristicValue(state):
    heuristic = int(math.ceil(ManhattanDistance(state)/3))
    return heuristic

lc = {}
def conflictsInRow(state, tile, rownumber):
    conflicts = 0
    row = state[rownumber]
    for i in range(0, len(row)-1):
        tj = row[i]
        tk = row[i+1]
        if goalStatePositions[tj][0] == goalStatePositions[tk][0]:
            if goalStatePositions[tj][1]>goalStatePositions[tk][1]:
                conflicts +=1
    return conflicts


def linearConflict(state):
    for i, row in state:
        lc[i] = 0
        for j, col in row:
            # find C(state[i][j],i)
            rowConflicts = conflictsInRow(state, state[i][j], i)



# # Gives the ceil value for misplacesTiles/3
# def heuristicValue(state):
#     state_flat_list = [item for element in state for item in element]
#     goal_flat_list = [item for element in goal_state[0] for item in element]
#     misplacedTiles = 0
#     for i in range(0, 16):
#         if state_flat_list[i] == 0:
#             continue
#         if state_flat_list[i] != goal_flat_list[i]:
#             misplacedTiles += 1
#     heuristic = int(math.ceil(misplacedTiles/3))
#     return heuristic

# returns a list of possible combinations for moving the tile Up with list of move
def MoveTileUp(puzzle, blankPosition, movesUntilNow, cost, succ):
    puzzleCopy = copy.deepcopy(puzzle)
    x = blankPosition[0][0]
    y = blankPosition[0][1]
    i = 0
    for index in range(x+1, 4):
        movesUntilNowCopy = copy.deepcopy(movesUntilNow)
        i = i+1
        puzzleCopy[index][y], puzzleCopy[index-1][y] = puzzleCopy[index-1][y], puzzleCopy[index][y]
        movesUntilNowCopy.append('U'+str(i)+str(y+1))
        succ.append([copy.deepcopy(puzzleCopy), movesUntilNowCopy, cost+1, cost + heuristicValue(puzzleCopy)])

# returns a list of possible combinations for moving the tile down with list of move
def MoveTileDown(puzzle, blankPosition, movesUntilNow, cost, succ):
    puzzleCopy = copy.deepcopy(puzzle)
    x = blankPosition[0][0]
    y = blankPosition[0][1]
    i = 0
    for index in range(x-1, -1, -1):
        movesUntilNowCopy = copy.deepcopy(movesUntilNow)
        i = i+1
        puzzleCopy[index][y], puzzleCopy[index+1][y] = puzzleCopy[index+1][y], puzzleCopy[index][y]
        movesUntilNowCopy.append('D'+str(i)+str(y+1))
        succ.append([copy.deepcopy(puzzleCopy), movesUntilNowCopy, cost + 1, cost + heuristicValue(puzzleCopy)])

# return returns a list of possible combinations for moving the tile down with list of move
def MoveTileRight(puzzle, blankPosition, movesUntilNow, cost, succ):
    puzzleCopy = copy.deepcopy(puzzle)
    x = blankPosition[0][0]
    y = blankPosition[0][1]
    i = 0
    for index in range(y-1, -1, -1):
        movesUntilNowCopy = copy.deepcopy(movesUntilNow)
        i = i+1
        puzzleCopy[x][index], puzzleCopy[x][index+1] = puzzleCopy[x][index+1], puzzleCopy[x][index]
        movesUntilNowCopy.append('R'+str(i)+str(x+1))
        succ.append([copy.deepcopy(puzzleCopy), movesUntilNowCopy, cost + 1, cost + heuristicValue(puzzleCopy)])

# returns a list of possible combinations for moving the tile Up with list of move
def MoveTileLeft(puzzle, blankPosition, movesUntilNow, cost, succ):
    puzzleCopy = copy.deepcopy(puzzle)
    x = blankPosition[0][0]
    y = blankPosition[0][1]
    i = 0
    for index in range(y+1, 4):
        movesUntilNowCopy = copy.deepcopy(movesUntilNow)
        i = i+1
        puzzleCopy[x][index], puzzleCopy[x][index-1] = puzzleCopy[x][index-1], puzzleCopy[x][index]
        movesUntilNowCopy.append('L'+str(i)+str(x+1))
        succ.append([copy.deepcopy(puzzleCopy), movesUntilNowCopy, cost + 1, cost + heuristicValue(puzzleCopy)])


#  returns a list of successors, which individually contains two list.
def successor(currentState):
    succ = []
    blankPosition = FindPositionOfBlankTile(currentState[0])
    MoveTileUp(currentState[0], blankPosition, currentState[1], currentState[2], succ)
    MoveTileDown(currentState[0], blankPosition, currentState[1], currentState[2], succ)
    MoveTileRight(currentState[0], blankPosition, currentState[1], currentState[2], succ)
    MoveTileLeft(currentState[0], blankPosition, currentState[1], currentState[2], succ)
    return succ

# returns true if current state is present in the fringe and also removes the larger cost state
def IsStateWithLargerTotalCostInFringe(current, fringe):
    for item in fringe:
        if item[0] == current[0]:
            oldCost = item[3]
            newCost = current[3]
            if oldCost > newCost:
                fringe.remove(item)
                return True

# Solve using A* algorithm 3
def solve(initial_state):
    # if IsParityInversionSatisfied(initial_state[0], goal_state[0]):
    if  initial_state[0] == goal_state[0]:
        return initial_state
    fringe = [initial_state]
    closed = []
    while len(fringe)>0:
        fringe = sorted(fringe, key = itemgetter(3))
        popped_fringe = fringe.pop(0)
        closed.append(popped_fringe)
        if popped_fringe[0] == goal_state[0]:
            return popped_fringe
        else:
            for s in successor(popped_fringe):
                if s in closed:
                    continue
                if s in fringe:
                    # find if s is in fringe with larger value of f(s)
                    if(IsStateWithLargerTotalCostInFringe(s, fringe)):
                        fringe.append(s)
                else:
                    fringe.append(s)
    return False
    # return False
# print "return IsStateWithLargerTotalCostInFringe is {0}".format(IsStateWithLargerTotalCostInFringe(currentState, fringe))
# print "fringe is {0}".format(fringe)

# print "successors of initial state are {0}".format(successor(initial_state))
# print "Length of successors of initial state is {0}".format(len(successor(initial_state)))
# print "successors of goal state are {0}".format(successor(goal_state))
# print "Length of successors of goal state is {0}".format(len(successor(goal_state)))
CreateGoalStatePositionsDictionary(goal_state[0])
solution = solve(initial_state)
if  solution == False:
    print "No solution"
else:
    print "solution reached in {0} steps".format(solution[2])
    print "solution reached in {0} moves".format(solution[1])


# # print "dictionary is {0}".format(goalStatePositions)
# print "MD for initial state is {0}".format(ManhattanDistance([[1,3,6,4],[5,11,2,8],[0,9,7,12],[13,10,14,15]]))
# print "Misplaced tile heuristic for initial state is {0}".format(heuristicValue([[1,3,6,4],[5,11,2,8],[0,9,7,12],[13,10,14,15]]))