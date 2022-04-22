from cmu_cs3_graphics import *
import random

# Watched https://www.youtube.com/watch?v=X3sYTrT-maA&ab_channel=TurkeyDev
# for idea of Prim's algorithm 

# Prim's algorithm with blocks instead of walls
# https://stackoverflow.com/questions/6083066/depth-first-search-maze-generation-algorithm-with-blocks-instead-of-walls

def maze(row,col):
    rows = row*2 + 1 
    cols = col*2 + 1 
    map = [[1]*cols for row in range(rows)]
    currentRow = 0
    currentCol = 0
    visited = [(currentRow,currentCol)]
    map[currentRow][currentCol] = 0
    toVisit = [(2,0),(0,2)]
    # stores all possible toVisit locations with corresponding visited location
    directionMap = {(2,0):(0,0),(0,2):(0,0)}

    while len(visited) == 1 or len(toVisit) > 0:
        index = random.randint(0,len(toVisit)-1)
        nextVisit = toVisit[index]
        toVisit.remove(nextVisit)
        if nextVisit in visited:
            continue

        map[nextVisit[0]][nextVisit[1]] = 0

        # calculate middle block location between jumps
        r,c = directionMap[nextVisit]
        wallRow = (max(nextVisit[0], r)) - 1
        wallCol = (max(nextVisit[1], c)) - 1
        if nextVisit[0] == r:
            wallRow = r
        if nextVisit[1] == c:
            wallCol = c
  
        map[wallRow][wallCol] = 0

        visited.append(nextVisit)

        # All potential directions: left, right, top, down
        # Record the location into the dictionary before making jump 
        directions = [(0,2),(2,0),(-2,0),(0,-2)]
        for (r,c) in directions:
            newRow = nextVisit[0] + r
            newCol = nextVisit[1] + c
            if (newRow >= 0 and newRow < rows and newCol >= 0 and newCol < cols):
                if map[newRow][newCol] == 1 and ((newRow,newCol) not in visited):
                    toVisit.append((newRow,newCol))
                    directionMap[(newRow,newCol)] = nextVisit

    # Add border around the map
    for cc in range(cols):
        map[cc].insert(0,1)
        map[cc].append(1)
    borderRow = [1 for row in range(rows+2)]
    map.insert(0,borderRow)
    map.append(borderRow)

    return map