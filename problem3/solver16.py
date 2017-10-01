#!/usr/bin/env python
# put your 15 puzzle solver here!
from operator import itemgetter
import copy
import math
import time
import sys

# State: [[[],[],[],[]], [moves to get to that state], c(s),f(s)]
initial_state = []
# initial_state = [[[5,1,2,3],[13,6,4,11],[10,9,15,0],[14,12,7,8]],[], 0, 0]
goal_state = [[[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 12], [13, 14, 15, 0]], []]
# fringe = [initial_state]
goalStatePositions = {}

# check of valid rows and col are provided
def CheckIfValidRowsAndColumn(puzzleboard):
    row = len(puzzleboard)
    if row != 4:
        return False
    for row in puzzleboard:
        col = len(row)
        if col != 4:
            return False

# check if valid tiles are present in puzzle
def CheckTilesInPuzzle(puzzleboard):
    puzzle_flat_list = [item for element in puzzleboard for item in element]
    status = all(item >= 0 or item < 16 for item in puzzle_flat_list)
    return status

# check duplicate tiles in board
def CheckDuplicateTiles(puzzleboard):
    puzzle_flat_list = [item for element in puzzleboard for item in element]
    return len(puzzle_flat_list) == len(set(puzzle_flat_list))

# check if valid input is provided
def IsInputValid(intial_state):
   return CheckIfValidRowsAndColumn(initial_state[0]) and \
            CheckTilesInPuzzle(initial_state[0]) and \
            CheckDuplicateTiles(initial_state[0])

# creates a dictionary for evry goal state tile position
def CreateGoalStatePositionsDictionary(goal):
    for i, row in enumerate(goal):
        for j, col in enumerate(row):
            goalStatePositions[goal[i][j]] = [i, j]

# generate parity for a particular state
def GenerateParity(state):
    parityInversion = 0
    i = 0
    j = 0
    flat_list = [item for element in state for item in element]
    for i in range(0, len(flat_list)):
        for j in range(i + 1, len(flat_list)):
            if flat_list[j] == 0 or flat_list[i] == 0:
                continue
            if flat_list[j] < flat_list[i]:
                parityInversion = parityInversion + 1
    return parityInversion

# check if parity inversion is satisfied
def IsParityInversionSatisfied(currentstate, goal_state):
    goalParity = GenerateParity(goal_state)
    stateparity = GenerateParity(currentstate)
    return (goalParity % 2) == (stateparity % 2)

# returns a position of blank tile in the given puzzle
def FindPositionOfBlankTile(puzzle):
    return [(row, col) for row in range(0, 4) for col in range(0, 4) if puzzle[row][col] == 0]

# returns the manhattan distance for the puzzle state
def ManhattanDistance(puzzle):
    manhattanDistance = 0
    for i, row in enumerate(puzzle):
        for j, col in enumerate(row):
            if col == 0:
                continue
            manhattanDistance = manhattanDistance + abs(goalStatePositions[col][0] - i) \
                                + abs(goalStatePositions[col][1] - j)
    return manhattanDistance

# returns number of conflicts in a particular row for a particular tile
def conflictsInRow(state, tile, tilerownumber, tilecolnumber):
    conflicts = 0
    row = state[tilerownumber]
    conflictedTilesInRow = []
    for k in range(0, len(row)):
        tj = tile
        tk = row[k]
        if tj != 0 and tk != 0:
            if goalStatePositions[tj][0] == goalStatePositions[tk][0]: # check if the 2 tiles are in same row in goal position
                if (tilecolnumber > k and goalStatePositions[tj][1] < goalStatePositions[tk][1]) \
                        or (tilecolnumber < k and goalStatePositions[tj][1] > goalStatePositions[tk][1]):
                    conflicts += 1
                    conflictedTilesInRow.append(tk)
    return conflicts, conflictedTilesInRow

# returns number of conflicts in a particular column for a particular tile
def conflictsInColumn(state, tile, tilerownumber, tilecolnumber):
    conflicts = 0
    conflictedTilesInColumn = []
    column = [row[tilecolnumber] for row in state]
    for k in range(0, len(column)):
        tj = tile
        tk = column[k]
        if tj != 0 and tk != 0:
            if goalStatePositions[tj][1] == goalStatePositions[tk][1]: # check if the 2 tiles are in same column in goal position
                if (tilerownumber > k and goalStatePositions[tj][0] < goalStatePositions[tk][0]) \
                        or (tilerownumber < k and goalStatePositions[tj][0] > goalStatePositions[tk][0]):
                    conflicts += 1
                    conflictedTilesInColumn.append(tk)
    return conflicts, conflictedTilesInColumn

# returns linear conflict for a particular state
def linearConflict(state, lc):
    for i, row in enumerate(state):
        lc[("row", i)] = 0
        rConflicts = {}
        for j, col in enumerate(row):
            rConflicts[(state[i][j], i)] = conflictsInRow(state, state[i][j], i, j)
        while max(rConflicts.iteritems(), key = lambda x: x[1][0])[1][0] > 0:
            keytk = max(rConflicts.iteritems(), key = itemgetter(1))[0]
            conflictedTilesWithtk = rConflicts[keytk][1]
            rConflicts[keytk] = [0, conflictedTilesWithtk]
            for tj in rConflicts[keytk][1]:
                rConflicts[(tj, i)] = rConflicts[(tj, i)][0] - 1, rConflicts[(tj, i)][1]
            lc[("row", i)] = lc[("row", i)] + 1

    for k in range(0, len(state[0])):
        lc[("col", k)] = 0
        cConflicts = {}
        for i, row in enumerate(state):
            cConflicts[(state[i][k], k)] = conflictsInColumn(state, state[i][k], i, k)
        while max(cConflicts.iteritems(), key=lambda x: x[1][0])[1][0] > 0:
            keytk = max(cConflicts.iteritems(), key=itemgetter(1))[0]
            conflictedTilesWithtk = cConflicts[keytk][1]
            cConflicts[keytk] = [0, conflictedTilesWithtk]
            for tj in cConflicts[keytk][1]:
                cConflicts[(tj, k)] = cConflicts[(tj, k)][0] - 1, cConflicts[(tj, k)][1]
            lc[("col", k)] = lc[("col", k)] + 1

    return sum(values[1] for values in lc.items())

# return heuristic value MD/3 plus linear conflicts
def heuristicValue(state):
    lc = {}
    MD = int(math.ceil(float(ManhattanDistance(state)) / 3))
    LC = (2 * linearConflict((state), lc))
    heuristic = MD + LC
    return heuristic

# check if a board configuration is present in fringe
def IsStateInClosed(current, closed):
    for item in closed:
        if item[0] == current[0]:
            return True
    return False

# returns a list of possible combinations for moving the tile Up with list of move
def MoveTileUp(puzzle, blankPosition, movesUntilNow, cost, succ):
    puzzleCopy = copy.deepcopy(puzzle)
    x = blankPosition[0][0]
    y = blankPosition[0][1]
    i = 0
    for index in range(x + 1, 4):
        movesUntilNowCopy = copy.deepcopy(movesUntilNow)
        i = i + 1
        puzzleCopy[index][y], puzzleCopy[index - 1][y] = puzzleCopy[index - 1][y], puzzleCopy[index][y]
        movesUntilNowCopy.append('U' + str(i) + str(y + 1))
        succ.append([copy.deepcopy(puzzleCopy), movesUntilNowCopy, cost + 1, cost + heuristicValue(puzzleCopy)])


# returns a list of possible combinations for moving the tile down with list of move
def MoveTileDown(puzzle, blankPosition, movesUntilNow, cost, succ):
    puzzleCopy = copy.deepcopy(puzzle)
    x = blankPosition[0][0]
    y = blankPosition[0][1]
    i = 0
    for index in range(x - 1, -1, -1):
        movesUntilNowCopy = copy.deepcopy(movesUntilNow)
        i = i + 1
        puzzleCopy[index][y], puzzleCopy[index + 1][y] = puzzleCopy[index + 1][y], puzzleCopy[index][y]
        movesUntilNowCopy.append('D' + str(i) + str(y + 1))
        succ.append([copy.deepcopy(puzzleCopy), movesUntilNowCopy, cost + 1, cost + heuristicValue(puzzleCopy)])

# return returns a list of possible combinations for moving the tile down with list of move
def MoveTileRight(puzzle, blankPosition, movesUntilNow, cost, succ):
    puzzleCopy = copy.deepcopy(puzzle)
    x = blankPosition[0][0]
    y = blankPosition[0][1]
    i = 0
    for index in range(y - 1, -1, -1):
        movesUntilNowCopy = copy.deepcopy(movesUntilNow)
        i = i + 1
        puzzleCopy[x][index], puzzleCopy[x][index + 1] = puzzleCopy[x][index + 1], puzzleCopy[x][index]
        movesUntilNowCopy.append('R' + str(i) + str(x + 1))
        succ.append([copy.deepcopy(puzzleCopy), movesUntilNowCopy, cost + 1, cost + heuristicValue(puzzleCopy)])

# returns a list of possible combinations for moving the tile Up with list of move
def MoveTileLeft(puzzle, blankPosition, movesUntilNow, cost, succ):
    puzzleCopy = copy.deepcopy(puzzle)
    x = blankPosition[0][0]
    y = blankPosition[0][1]
    i = 0
    for index in range(y + 1, 4):
        movesUntilNowCopy = copy.deepcopy(movesUntilNow)
        i = i + 1
        puzzleCopy[x][index], puzzleCopy[x][index - 1] = puzzleCopy[x][index - 1], puzzleCopy[x][index]
        movesUntilNowCopy.append('L' + str(i) + str(x + 1))
        succ.append([copy.deepcopy(puzzleCopy), movesUntilNowCopy, cost + 1, cost + heuristicValue(puzzleCopy)])

# returns a list of successors, which individually contains two list.
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
    return False

# solve using A* algorithm 3
def solve(initial_state):
    if initial_state[0] == goal_state[0]:
        return initial_state
    fringe = [initial_state]
    closed = []
    while len(fringe) > 0:
        fringe = sorted(fringe, key=itemgetter(3))
        popped_fringe = fringe.pop(0)
        if not IsStateInClosed(popped_fringe, closed):
            closed.append(popped_fringe)
            if popped_fringe[0] == goal_state[0]:
                return popped_fringe
            for s in successor(popped_fringe):
                fringe.append(s)
    return False


filename = sys.argv[1]
with open(filename, 'r') as file:
    initial_board = []
    for line in file:
        row = []
        for col in line.strip().split(" "):
            try:
                row.append(int(col))
            except ValueError:
                print "Enter valid number"
        initial_board.append(row)
    initial_state.append(initial_board)

initial_state.append([])
initial_state.append(0)
initial_state.append(0)

CreateGoalStatePositionsDictionary(goal_state[0])
solution = solve(initial_state)
if  solution == False:
    print "No solution"
else:
    print " ".join([str(x) for x in solution[1]])




