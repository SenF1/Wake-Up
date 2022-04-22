from pathfinding import pathSolution

# Enemies Generation

class enemie(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y

solution = pathSolution(map,(1,1),(playerx,playery),mapSize,mapSize)
