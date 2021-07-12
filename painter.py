import cv2
import numpy as np
import time
import os
import HandTrackingModule as htm

cap = cv2.VideoCapture(0)
cap.set(3,1280)
cap.set(4, 720)
detector = htm.handDetector(detectionCon=0.85)

#Creat a retangle for selection with middle of xy and corner length of l and side length of r and tickness of t
def select_color(x,y,l=2,r=25,t=2):
    #Top left corner
    cv2.line(img, (x-r,y-r), (x-r+l, y-r),(0,0,0), t) #(img, starting point)
    cv2.line(img, (x-r,y-r), (x-r, y-r+l),(0,0,0), t)

    #Top right corner
    cv2.line(img, (x+r,y-r), (x+r-l, y-r),(0,0,0), t) #(img, starting point)
    cv2.line(img, (x+r,y-r), (x+r, y-r+l),(0,0,0), t)

    #Bottom left
    cv2.line(img, (x-r,y+r), (x-r+l, y+r),(0,0,0), t) #(img, starting point)
    cv2.line(img, (x-r,y+r), (x-r, y+r-l),(0,0,0), t) 

    #Bottom right
    cv2.line(img, (x+r,y+r), (x+r-l, y+r),(0,0,0), t) #(img, starting point)
    cv2.line(img, (x+r,y+r), (x+r, y+r-l),(0,0,0), t)

drawColor = (255,255,255)
brushThickness = 20
eraserTickness = 50
xp, yp =0, 0

imgCanvas = np.zeros((720, 1280, 3), np.uint8)

while True:
    success, img = cap.read()

    img = cv2.flip(img, 1)

    #cv2.rectangle(img, (0,0), (1280,80), (255,255,255), cv2.FILLED) #Menu bar
    cv2.circle(img, (150, 35), 25, (247,121,4), cv2.FILLED) #Blue
    cv2.circle(img, (350, 35), 25, (4,9,247), cv2.FILLED) #Red
    cv2.circle(img, (550, 35), 25, (36,205,255), cv2.FILLED) #Yellow
    cv2.circle(img, (750, 35), 25, (3,179,86), cv2.FILLED) #Green 
    cv2.circle(img, (950, 35), 25, (100,100,100), cv2.FILLED) #Grey
    cv2.circle(img, (1150, 35), 25, (100,100,100), 2) #Eraser
    # cv2.putText(img, "E", (1120,60), cv2.FONT_HERSHEY_SIMPLEX, 2.2, color=(0,0,0), thickness=6) #Eraser

    # Find hand landmarks
    img = detector.findHands(img)
    lmList = detector.findPosition(img, draw = True)
    if len(lmList) != 0:
        x1, y1 = lmList[8][1:] # tip of index figer
        x2, y2 = lmList[12][1:] # tip of middle figer
    
        # Check with finger(s) is up
        fingers = detector.fingersUp()

        # If selection mode -  two finger are up
        if fingers == [False, True, True, False, False]:
            xp, yp =0, 0
            x_s, y_s = (x1+x2)/2, (y1+y2)/2
            #Checking for the selection
            if y_s < 80:
                if 125 < x_s < 175:
                    select_color(150, 40)
                    drawColor = (247,121,4)
                elif 325 < x_s < 375:
                    select_color(350, 40)
                    drawColor = (4,9,247)
                elif 525 < x_s < 575:
                    select_color(550, 40)
                    drawColor = (36,205,255)
                elif 725 < x_s < 775:
                    select_color(750, 40)
                    drawColor = (3,179,86)
                elif 925 < x_s < 975:
                    select_color(950, 40)
                    drawColor = (100,100,100)
                elif 1125 < x_s < 1175:
                    select_color(1150, 40)
                    drawColor = (0,0,0)
            cv2.circle(img, (int(x_s), int(y_s)), 10, drawColor, cv2.FILLED)
        
        # If Drawing mode -index finger is up
        if fingers == [False, True, False, False, False]:
            
            cv2.circle(img, (x1, y1), 10, drawColor, cv2.FILLED)
            if xp==0 and yp==0: #when initial entering into the draw model draw a dot
                xp, yp = x1, y1
            # Then you simply draw lines from the previous point to the current potin 
            if drawColor == (0,0,0):
                cv2.line(img, (xp,yp), (x1,y1), drawColor, eraserTickness)
                cv2.line(imgCanvas, (xp,yp), (x1,y1), drawColor, eraserTickness)
            else:
                cv2.line(img, (xp,yp), (x1,y1), drawColor, brushThickness)
                cv2.line(imgCanvas, (xp,yp), (x1,y1), drawColor, brushThickness) 
            # Update the previous point to curnet at FPS rate
            xp, yp = x1, y1

    # Convert the Canvas img to Grey img
    imgGray = cv2.cvtColor(imgCanvas, cv2.COLOR_BGR2GRAY)
    # Reverse the Grey img to a black and white img, with white as background and black as the drawing color
    _, imgInv = cv2.threshold(imgGray, 50,255,cv2.THRESH_BINARY_INV)
    imgInv = cv2.cvtColor(imgInv, cv2.COLOR_GRAY2BGR)

    # Add the Reverse img to the original img, so the black will be left
    img = cv2.bitwise_and(img, imgInv)

    # Add the Canvas image with color to the img, to fill the black
    img = cv2.bitwise_or(img, imgCanvas)

    cv2.imshow("Image", img)
    # img = cv2.addWeighted(img, 0.5, imgCanvas, 0.5, 0)
    cv2.imshow("Canvas", imgCanvas)
    cv2.waitKey(1)