from cmu_cs3_graphics import *
import math


def onAppStart(app): 
    app.playerx = 100
    app.playery = 100
    app.player_angle = math.pi
    app.mapSize = 10
    app.cellSize = (app.width/2)/app.mapSize-20
    app.map = [
        '1111111111',
        '1000110111',
        '1000010111',
        '1110000111',
        '1010000111',
        '1010000111',
        '1000000011',
        '1000000011',
        '1222111111',
        '1111111111',
    ]
    app.height = 720
    app.width = 1280
    app.FOV= math.pi/3
    app.castedRays = 120
    app.stepAngle = app.FOV/app.castedRays
    app.maxDepth = int(app.cellSize*app.mapSize)
    app.scale = (app.width/2)/app.castedRays

#raycasting
def rayCasting(app):
    #Start from leftmost angle and increment
    startAngle = app.player_angle-app.FOV/2
    for ray in range(app.castedRays):
        for depth in range(app.maxDepth):
            targetx = app.playerx-math.sin(startAngle) * depth
            targety = app.playery+math.cos(startAngle) * depth

            col = int(targetx/ app.cellSize)
            row = int(targety/ app.cellSize)
            if app.map[row][col] == '1':
                #highlight 2d hitted walls
                drawRect(col*app.cellSize, row*app.cellSize, app.cellSize, app.cellSize, fill='lightgreen')
                drawLine(app.playerx, app.playery, targetx, targety, fill='red',lineWidth=3)
                
                #shading
                color = int(255/((depth**2)*0.0001+1))

                #calculate wall height: determines the distance from view to wall
                wallHeight = 30000/(depth+1)

                #Keep wallheight at maximum of screen height
                if wallHeight > app.height:
                    wallHeight = app.height

                #draw walls
                drawRect(app.height*3/4 + ray * app.scale, (app.height/2)-wallHeight/2, 
                app.scale, wallHeight,fill=rgb(color, color, color))
                break
        startAngle+=app.stepAngle

#draw map
def drawMap(app):
    for row in range(app.mapSize):
        for col in range(app.mapSize):
            if app.map[row][col] == '1':
                drawRect(col*app.cellSize, row*app.cellSize,app.cellSize, app.cellSize, fill='lightgrey')
            else:
                drawRect(col*app.cellSize, row*app.cellSize,app.cellSize, app.cellSize, fill='grey')

def checkCollision(app, direction):
    col = int(app.playerx/ app.cellSize)
    row = int(app.playery/ app.cellSize)
    if app.map[row][col] == '1':
        if direction == 'up':
            app.playerx -= -math.sin(app.player_angle) * 10
            app.playery -= math.cos(app.player_angle) * 10
        else:
            app.playerx += -math.sin(app.player_angle) * 10
            app.playery += math.cos(app.player_angle) * 10

def onKeyPress(app, key):
    if key == 'left':
        app.player_angle -= 0.3
    elif key == 'right':
        app.player_angle += 0.3
    elif key == 'up':
        app.playerx += -math.sin(app.player_angle) * 10
        app.playery += math.cos(app.player_angle) * 10
        checkCollision(app, 'up')
    elif key == 'down':
        app.playerx -= -math.sin(app.player_angle) * 10
        app.playery -= math.cos(app.player_angle) * 10
        checkCollision(app,'down')

def redrawAll(app):
    #update 2d background
    drawRect(0,0,app.height,app.height)

    #update 3d background
    drawRect(0,0,app.width,app.height/2,fill='grey')
    drawRect(0,app.height/2,app.width,app.height/2,fill='lightgrey')

    #draw 2d map
    drawMap(app)

    #draw player on board
    drawCircle(app.playerx,app.playery,4,fill='yellow')

    #raycasting
    rayCasting(app)
    
def main():
    runApp(width=1280, height=720)

main()