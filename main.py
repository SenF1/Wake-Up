from cmu_cs3_graphics import *
import math
import random
from PIL import Image, ImageTk
from mazeGeneration import maze
from pathfinding import pathSolution

def onAppStart(app): 
    app.playerx = 40
    app.playery = 40
    app.playerAngle = 0
    app.mazeSize = 3
    app.mapSize = app.mazeSize*2+3
    app.cellSize = app.width/50
    app.map = maze(app.mazeSize, app.mazeSize)
    app.count = 0

    # Set starting point and winning location
    winLocation = False
    app.end = (8,8)
    # Finding a winning location that is the farthest 
    for row in range(app.mapSize-1,-1,-1):
        for col in range(app.mapSize-1,-1,-1):
            if winLocation == False:
                if (app.map[row][col] == 0):
                    directions = [(0,1),(1,0),(-1,0),(0,-1),(1,1),(-1,-1)]
                    count = 0
                    for (r,c) in directions:
                        newRow = row + r
                        newCol = col + c     
                        if (newRow >= 0 and newRow < app.mapSize and newCol >= 0 and newCol < app.mapSize):
                            if app.map[newRow][newCol] == 1:
                                count+=1
                    if count == 5:
                        winLocation = True
                        app.end = (row,col)
                        break
    if app.end != None:
        app.solution = pathSolution(app.map,(1,1),app.end,app.mapSize,app.mapSize)
        for (r,c) in app.solution:
            app.map[r][c] = 5
    
    # Initialize start and end position
    app.map[1][1] == 2
    app.map[app.end[0]][app.end[1]] = 3

    # Change to string since the numbers was in int for locating purpose
    for row in range(app.mapSize):
        for col in range(app.mapSize):
            app.map[row][col] = str(app.map[row][col])


    app.height = 720
    app.width = 1280
    app.FOV= math.pi/2
    app.castedRays = 200
    app.stepAngle = app.FOV/app.castedRays
    app.maxDepth = int(app.cellSize*app.mapSize)
    app.scale = app.width/app.castedRays
    app.moveSpeed = 3

    # For mouse and jumping
    app.prevx = 0
    app.prevy = 0
    app.playerAngleY = 0
    app.playerWin = False
    app.playerHeight = 1
    app.playerJump = False

    app.enemyx = 40
    app.enemyy = 60

# Control angle with mouse
# def onMouseMove(app, mousex, mousey):
#     if app.prevx != 0:
#         angleDiff = app.prevx - mousex
#         if angleDiff < 0:
#             app.playerAngle += abs(angleDiff*0.005)
#         else:
#             app.playerAngle -= abs(angleDiff*0.005)
#     app.prevx = mousex

#     if app.prevy != 0:
#         angleDiff = app.prevy - mousey
#         if angleDiff < 0:
#             app.playerAngleY -= abs(angleDiff) * 5
#             if abs(app.playerAngleY) > app.height/10:
#                 app.playerAngleY += abs(angleDiff) * 5
#         else:
#             app.playerAngleY += abs(angleDiff) * 5
#             if abs(app.playerAngleY) > app.height/10:
#                 app.playerAngleY -= abs(angleDiff) * 5
#     app.prevy = mousey

def playerWon(app):
    drawLabel('You Win',app.width/2,app.height/2,size=200)
    


#Raycasting concepts are from:
# https://lodev.org/cgtutor/raycasting.html#Introduction
# https://www.youtube.com/watch?v=LUYxLjic0Bc&t=300s 
# https://www.youtube.com/watch?v=gYRrGTC7GtA&ab_channel=3DSage
# https://www.youtube.com/watch?v=PC1RaETIx3Y&ab_channel=3DSage 
# https://www.youtube.com/watch?v=LUYxLjic0Bc&t=300s&ab_channel=Kofybrek 
# https://scs.hosted.panopto.com/Panopto/Pages/Viewer.aspx?id=ad65db4c-e9a1-449c-a50b-ae6a005c256d

def rayCasting(app):
    #Start from leftmost angle and increment
    startAngle = app.playerAngle-app.FOV/2
    for ray in range(app.castedRays):
        for depth in range(app.maxDepth):
            targetx = app.playerx-math.sin(startAngle) * depth
            targety = app.playery+math.cos(startAngle) * depth

            col = int(targetx/ app.cellSize)
            row = int(targety/ app.cellSize)

            # Ememy rol and col
            enemyCol = int(app.enemyx/ app.cellSize)
            enemyRow = int(app.enemyy/ app.cellSize)
            
            if app.map[row][col] == '1':
                # Highlight 2d hitted walls
                # drawRect(col*app.cellSize, row*app.cellSize, app.cellSize, app.cellSize, fill='lightgreen')
                # drawLine(app.playerx, app.playery, targetx, targety, fill='red',lineWidth=3)

                # Fix fisheye
                depth *= math.cos(app.playerAngle-startAngle)

                # Shading
                color = int(255/((depth**2)*0.0001+1))

                # Calculate wall height: determines the distance from view to wall
                wallHeight = (app.cellSize*app.height)/depth + 100

                #Keep wallheight at maximum of screen height
                if wallHeight > app.height:
                    wallHeight = app.height
                
                #offset
                offset = (app.height/2)-wallHeight/2

                #draw walls  
                drawRect(ray * app.scale,offset+app.playerHeight+app.playerAngleY, 
                app.scale*2, wallHeight,fill=rgb(color,color,color))
                break
            # if app.map[row][col] == '0' and row == enemyRow and col == enemyCol:
            #     drawCircle(row,col, ray,fill='red')
        startAngle+=app.stepAngle

#draw map
def drawMap(app):
    for row in range(app.mapSize):
        for col in range(app.mapSize):
            if app.map[row][col] == '1':
                drawRect(col*app.cellSize,row*app.cellSize,app.cellSize, app.cellSize, fill='lightgrey')
            elif app.map[row][col] == '2':
                drawRect(col*app.cellSize,row*app.cellSize,app.cellSize, app.cellSize, fill='green')
            elif app.map[row][col] == '3':
                drawRect(col*app.cellSize,row*app.cellSize,app.cellSize, app.cellSize, fill='green')
            elif app.map[row][col] == '5':
                drawRect(col*app.cellSize,row*app.cellSize,app.cellSize, app.cellSize, fill='green')
            else:
                drawRect(col*app.cellSize,row*app.cellSize, app.cellSize,app.cellSize, fill='grey')


def checkCollision(app, direction):
    col = int(app.playerx/ app.cellSize)
    row = int(app.playery/ app.cellSize)
    # Undo if hit wall, based on direction
    if app.map[row][col] == '1':
        if direction == 'up':
            app.playerx -= -math.sin(app.playerAngle) * app.moveSpeed
            app.playery -= math.cos(app.playerAngle) * app.moveSpeed
        else:
            app.playerx += -math.sin(app.playerAngle) * app.moveSpeed
            app.playery += math.cos(app.playerAngle) * app.moveSpeed

def onStep(app):
    app.moveSpeed = 3
    c = int(app.playerx/app.cellSize)
    r = int(app.playery/app.cellSize)
    if app.map[r][c] == '3':
        app.playerWin = True

    if app.playerJump:
        app.playerHeight *= 1.5
    else:
        if app.playerHeight > 1:
            app.playerHeight *= 0.7
        elif app.playerHeight < 1:
            app.playerHeight = 1

    if app.playerHeight > 100:
        app.playerJump = False

def onKeyPress(app,key):
    if app.playerWin == False:
        if key == 'space':
            if app.playerHeight == 1:
                app.playerJump = True


def onKeyHold(app, keys):
    if app.playerWin == False:
        if 'a' in keys:
            app.playerAngle -= 0.1
        if 'd' in keys:
            app.playerAngle += 0.1
        if 'w' in keys:
            app.playerx += -math.sin(app.playerAngle) * app.moveSpeed
            app.playery += math.cos(app.playerAngle) * app.moveSpeed
            checkCollision(app, 'up')
        if 's' in keys:
            app.playerx -= -math.sin(app.playerAngle) * app.moveSpeed
            app.playery -= math.cos(app.playerAngle) * app.moveSpeed
            checkCollision(app,'down')
        if 'shift' in keys:
            app.moveSpeed = 8
            print('1')

def redrawAll(app):
    #update background: top and bottom
    drawRect(0,0,app.width,app.height/2,fill='peru')
    drawRect(0,app.height/2,app.width,app.height/2,fill='sienna')

    #raycasting
    rayCasting(app)

    if app.playerWin == True:
        playerWon(app)

    #draw Map
    drawMap(app)
    
    #draw player and enemy on map
    drawCircle(app.playerx,app.playery,4,fill='yellow')
    drawCircle(app.enemyx,app.enemyy,4,fill='red')


def main():
    runApp(width=1280, height=720)

main()