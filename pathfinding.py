import math

# Watched: https://www.youtube.com/watch?v=-L-WgKMFuhE&ab_channel=SebastianLague
#          https://www.youtube.com/watch?v=aKYlikFAV4k
# Sources: http://theory.stanford.edu/~amitp/GameProgramming/AStarComparison.html#the-a-star-algorithm

def pathSolution(maze, start, end, rows, cols):
    start = (start[0], start[1], 0, None)
    end = (end[0], end[1], 0, None)
    toVisit = []
    visited = []
    directionMap = dict()

    toVisit.append(start)
    # Get the node with lowest f 
    while len(toVisit) > 0:
        current = toVisit[0]
        for node in toVisit:
            if node[2] < current[2]:
                current = node
        toVisit.remove(current)
        visited.append(current)
        if current == end:
            path = []
            while current != None:
                path.append((current[0],current[1]))
                current = directionMap[current[3]]
            return path
        # All potential directions: left, right, top, down
        directions = [(0,1),(1,0),(-1,0),(0,-1)]
        for (r,c) in directions: 
            newRow = current[0] + r
            newCol = current[1] + c
            if (newRow >= 0 and newRow < rows and newCol >= 0 and newCol < cols):
                if maze[newRow][newCol] == 0:
                    g = math.dist((start[0],start[1]),(newRow,newCol))
                    h = math.dist((end[0],end[1]),(newRow,newCol))
                    f = g+h
                    newNode = (newRow,newCol,f,current)
                    check = False
                    for node in toVisit:
                        if node[0] == newRow and node[1] == newCol:
                            directionMap[node] = current
                            node = (newRow,newCol,f,current)
                            check = True
                    if check == False:
                        toVisit.append(newNode)
                        directionMap[newNode] = current


    
