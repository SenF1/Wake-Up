from cmu_cs3_graphics import *
import pygame
import math, random
from PIL import Image, ImageDraw
from mazeGeneration import maze
from pathfinding import pathSolution


def onAppStart(app): 
    app.page = 'home'
    app.gameMode = 'easy'
    app.mazeSize = 3

    # player and map setup
    app.playerx = 40
    app.playery = 40
    app.playerAngle = 0
    app.mapSize = app.mazeSize*2+3
    app.cellSize = app.width/50
    app.map = []

    # Set starting point and winning location
    app.winSurrounding = []

    # Finding a winning location that is the farthest 
    app.end = []
    app.solution = []
    
    # Images
    # https://www.google.com/url?sa=i&url=https%3A%2F%2Fmedium.com%2F%40jpviergutz007%2F6-ways-to-wake-up-earlier-and-beat-the-alarm-clock-b23b1173af17&psig=AOvVaw3BTymhEy9pFcPxOuODZXlA&ust=1651099455684000&source=images&cd=vfe&ved=0CAwQjRxqFwoTCNDS8bnnsvcCFQAAAAAdAAAAABAJ
    app.homeUnedited = Image.open('homeUnedited.png')
    app.homeUnedited = CMUImage(app.homeUnedited.resize((480,400))) 

    app.home = Image.open('home.png')
    app.home = CMUImage(app.home.resize((1280,720)))

    app.select = Image.open('select.png')
    app.select = CMUImage(app.select.resize((1280,720)))

    # https://www.webnots.com/download-free-keyboard-key-images-in-black/ 
    app.guide = Image.open('guide.png')
    app.guide = CMUImage(app.guide.resize((480,270)))

    # https://icons8.com/icons/set/settings 
    app.setting = Image.open('setting.png')
    app.setting = CMUImage(app.setting.resize((50,50)))

    # Raycasting setup
    app.FOV= math.pi/2
    app.castedRays = 200
    app.stepAngle = app.FOV/app.castedRays
    app.maxDepth = int(app.width)
    app.scale = app.width/app.castedRays
    app.moveSpeed = 3

    # For mouse and jumping
    app.prevx = 0
    app.prevy = 0
    app.playerAngleY = 0
    app.playerWin = False
    app.playerHeight = 1
    app.playerJump = False

    app.showGuide = True
    app.showMap = False
    app.hint = 0
    app.hints = list()

    # Sounds
    app.stepsPerSecond = 10
    app.step = 39
    pygame.mixer.init()

    # https://djlunatique.com/iphone-alarm-radar-sound-effect/
    app.alarm = Sound("alarm.mp3")

    app.endPlay = True
    # https://www.myinstants.com/instant/rap-battle-ooohhhh/
    app.turnedOff = pygame.mixer.Sound("ohhh.mp3")

    app.startPlay = True
    # https://www.fesliyanstudios.com/royalty-free-music/downloads-c/peaceful-and-relaxing-music/22
    app.quietTime = pygame.mixer.Sound("quietTime.mp3")


def mazeSetup(app):
    app.mapSize = app.mazeSize*2+3
    app.map = maze(app.mazeSize, app.mazeSize)
    while len(app.map) == 0:
        app.map = maze(app.mazeSize, app.mazeSize)

    # Finding a winning location that is the farthest 
    app.end = findEnd(app)
    
    # In case there is no solution
    app.solution = pathSolution(app.map,(1,1),app.end)
    if app.solution == None:
        mazeSetup(app)

    for (r,c) in app.solution:
        app.map[r][c] = 5

    # Mark the surroundings of the goal location
    for (row, col) in app.winSurrounding:
        app.map[row][col] = 6

    # Initialize end position
    app.map[app.end[0]][app.end[1]] = 3

    # player starting angle
    if app.map[2][1] == 1:
        app.playerAngle = 30
    

def findEnd(app):
    directions = [(0,1),(1,0),(-1,0),(0,-1),(1,1),(-1,-1)]
    for col in range(app.mapSize-1,-1,-1):
        for row in range(app.mapSize-1,-1,-1):
            if (app.map[row][col] == 0):
                count = 0
                app.winSurrounding = []
                for (r,c) in directions:
                    newRow = row + r
                    newCol = col + c     
                    if (newRow >= 1 and newRow < app.mapSize-1 and newCol >= 1 and newCol < app.mapSize-1):
                        if app.map[newRow][newCol] == 1:
                            direction = [(0,1),(1,0),(-1,0),(0,-1)]
                            if (r,c) in direction:
                                app.winSurrounding.append((newRow,newCol))
                            count+=1
                if count == 5:
                    return (row,col)
    return None


class Sound(object):
    def __init__(self, path):
        self.path = path
        self.loops = 1
        pygame.mixer.music.load(path)

    # Loops = number of times to loop the sound.
    def start(self, loops=1):
        self.loops = loops
        pygame.mixer.music.play(loops=loops)

    # Stops the current sound from playing
    def stop(self):
        pygame.mixer.music.stop()


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
            
            if app.map[row][col] == 1 or app.map[row][col] == 6: 
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
                if app.map[row][col] == 1:
                    drawRect(ray * app.scale,offset+app.playerHeight+app.playerAngleY, 
                    app.scale*2, wallHeight,fill=rgb(color,color,color))
                elif app.map[row][col] == 6:
                    drawRect(ray * app.scale,offset+app.playerHeight+app.playerAngleY, 
                    app.scale*2, wallHeight,fill=rgb(color,255,color))
                break
        startAngle+=app.stepAngle


#draw map
def drawMap(app):
    for row in range(app.mapSize):
        for col in range(app.mapSize):
            if (row,col) in app.hints:
                drawRect(col*app.cellSize,row*app.cellSize,app.cellSize, app.cellSize, fill='green')
            elif app.map[row][col] == 1 or app.map[row][col] == 6:
                drawRect(col*app.cellSize,row*app.cellSize,app.cellSize, app.cellSize, fill='lightgrey')
            else:
                drawRect(col*app.cellSize,row*app.cellSize, app.cellSize,app.cellSize, fill='grey')

def checkCollision(app, direction):
    col = int(app.playerx / app.cellSize)
    row = int(app.playery / app.cellSize)
    # Undo if hit wall, based on direction
    if app.map[row][col] == 1 or app.map[row][col] == 6:
        if direction == 'up':
            app.playerx -= -math.sin(app.playerAngle) * app.moveSpeed
            app.playery -= math.cos(app.playerAngle) * app.moveSpeed
        else:
            app.playerx += -math.sin(app.playerAngle) * app.moveSpeed
            app.playery += math.cos(app.playerAngle) * app.moveSpeed


def onStep(app):
    if app.page == 'gaming':
        if app.startPlay == False:
            pygame.mixer.pause()
            app.startPlay = True
        app.step += 1
        if app.step == 40:
            app.alarm.start()
        app.step%=40

        distance = math.dist((app.playerx,app.playery),(app.end[0]*app.cellSize,app.end[1]*app.cellSize))
        volume = ((app.mapSize*4)/(distance))
        pygame.mixer.music.set_volume(volume)

        app.moveSpeed = 3
        c = int(app.playerx/app.cellSize)
        r = int(app.playery/app.cellSize)

        if app.map[r][c] == 3:
            app.playerWin = True
            app.alarm.stop()
            if app.endPlay:
                app.turnedOff.play()
                app.endPlay = False

        # Gives the ability to jump
        if app.playerJump:
            app.playerHeight *= 1.5
        else:
            if app.playerHeight > 1:
                app.playerHeight *= 0.7
            elif app.playerHeight < 1:
                app.playerHeight = 1

        if app.playerHeight > 100:
            app.playerJump = False
    else:
        if app.startPlay:
            app.quietTime.play()
            app.startPlay = False


def onMousePress(app,mouseX,mouseY):
    if app.page == 'home':
        if 525<mouseX<823 and 499<mouseY<564:
            app.page = 'select'
    elif app.page == 'select':
        if 582<mouseX<770 and 400<mouseY<469:
            app.gameMode = 'easy'
            app.mazeSize = 4
            mazeSetup(app) 
            app.page = 'gaming'
        elif 525<mouseX<823 and 498<mouseY<565:
            app.gameMode = 'medium'
            app.mazeSize = 8
            mazeSetup(app) 
            app.page = 'gaming'
        elif 581<mouseX<790 and 591<mouseY<657:
            app.gameMode = 'hard'
            app.mazeSize = 12
            mazeSetup(app)    
            app.page = 'gaming'
    elif app.page == 'gaming':
        if 1200<mouseX<1250 and 30<mouseY<72:
            app.showGuide = not app.showGuide
        if app.playerWin:
            if 608<mouseX<757 and 496<mouseY<542:
                onAppStart(app)


def onKeyPress(app,key):
    if app.page == 'gaming':
        app.showGuide = False
        if app.playerWin == False:
            if key == 'space':
                if app.playerHeight == 1:
                    app.playerJump = True
            elif key == 'e':
                app.showMap = not app.showMap
            elif key == 'h':
                if app.hint < len(app.solution):
                    app.hints.append(app.solution[app.hint])
                    app.hint+=1


def onKeyHold(app, keys):
    if app.page == 'gaming':
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

def gaming(app):
    #update background: top and bottom
    drawRect(0,0,app.width,app.height/2,fill='peru')
    drawRect(0,app.height/2,app.width,app.height/2,fill='sienna')

    #raycasting
    rayCasting(app)

    #draw Map
    if app.showMap:
        drawMap(app)
        #draw player on map
        drawCircle(app.playerx,app.playery,4,fill='yellow')


def redrawAll(app):
    if app.page == 'home':
        drawImage(app.home,0,0)
    elif app.page == 'select':
        drawImage(app.select,0,0)
    elif app.page == 'gaming':
        gaming(app)
        drawImage(app.setting,1200,30)
        if app.showGuide:
            drawImage(app.guide,app.width/2-200,app.height/2-100)
        if app.playerWin:
            drawImage(app.homeUnedited,app.width/2-200,app.height/2-200)
        if app.playerJump:
            drawLabel('Jump won\'t help, you are too short!',app.width/2,app.height/2,
            font='orbitron',size=20)

def main():
    runApp(width=1280, height=720)

if __name__ == '__main__':
    main()