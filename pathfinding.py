import math

# Watched: https://www.youtube.com/watch?v=-L-WgKMFuhE&ab_channel=SebastianLague
# Sources: http://theory.stanford.edu/~amitp/GameProgramming/AStarComparison.html#the-a-star-algorithm

def pathSolution(maze, start, end, rows, cols):
    startNode = (start[0], start[1], 0)
    toVisit = []
    visited = []
    toVisit.append(startNode)
    directionMap = {startNode:None}
    
    # Get the node with lowest f 
    while len(toVisit) > 0:
        current = toVisit[0]
        if len(toVisit) > 1:
            for someNode in toVisit:
                if someNode[2] < current[2]:
                    current = someNode
        toVisit.remove(current)

        # Find path
        if current[0]==end[0] and current[1]==end[1]:
            path = []
            while directionMap[current]:
                path.append((current[0],current[1]))
                current = directionMap.get(current)
            return path

        visited.append(current)
        # All potential directions: left, right, top, down
        directions = [(0,1),(1,0),(-1,0),(0,-1)]
        for (r,c) in directions: 
            newRow = current[0] + r
            newCol = current[1] + c
            if (newRow >= 0 and newRow < rows and newCol >= 0 and newCol < cols):
                if maze[newRow][newCol] == 0:
                    # Calculate all the values
                    g = math.dist((start[0],start[1]),(newRow,newCol))
                    h = math.dist((end[0],end[1]),(newRow,newCol))
                    f = int((g+h)*10)
                    newNode = (newRow,newCol,f)
                    if newNode not in toVisit:
                        if newNode not in visited:
                            toVisit.append(newNode)
                            directionMap[newNode] = (current[0],current[1],current[2])
