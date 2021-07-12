import cv2
import time
import numpy as np
import math
import HandTrackingModule as htm
##########################
wCam, hCam = 640, 480
##########################
cap = cv2.VideoCapture(0)
cap.set(3, wCam)
cap.set(4, hCam)
pTime = 0

detector = htm.handDetector(detectionCon=0.7)

while True:
    success, img = cap.read()
    
    img = detector.findHands(img)
    lmList = detector.findPosition(img, draw = True)

    if len(lmList) !=0:
        fingers = detector.fingersUp()
        totalFinger = fingers.count(True)
        #Print the number on the screen
        cv2.rectangle(img, (525,365), (625,465), (233,231,223), cv2.FILLED)
        cv2.putText(img, str(totalFinger), (550,440), cv2.FONT_HERSHEY_SIMPLEX, 2.5, (155,106,71), 7)
    
    cTime = time.time()
    fps = 1/(cTime-pTime)
    pTime = cTime
    cv2.rectangle(img, (483,15), (625,52), (111,106,71), cv2.FILLED)
    cv2.putText(img, f'FPS: {int(fps)}', (515,41), cv2.FONT_HERSHEY_SIMPLEX, 0.65, (255,255,255), 2)
    
    cv2.imshow("Img", img)
    cv2.waitKey(1)