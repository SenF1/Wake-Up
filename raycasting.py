from cmu_cs3_graphics import *
import math

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