"""
This is to test the module write in other py file can be reusable.
"""
import cv2
import mediapipe as mp
import time

import HandTrackingModule as htm

cap = cv2.VideoCapture(0) #Create the video capture object
    
pTime = 0 #previous time
cTime = 0 #current time

detector = htm.handDetector() #Create the detector object based on the class above

while True:
    sucess, img = cap.read()

    img = detector.findHands(img)
    lmList = detector.findPosition(img)
    if len(lmList) !=0: #In case the hand is not showing in the video yet
        print(lmList[8])
    cTime = time.time()

    fps = 1/(cTime-pTime)
    pTime = cTime

    cv2.putText(img, str(int(fps)), (10,70), cv2.FONT_HERSHEY_PLAIN, 3, color=(255,0,255), thickness=3) #Display the FPS on the screen, agruments at https://www.geeksforgeeks.org/python-opencv-cv2-puttext-method/

    cv2.imshow("Image", img)
    cv2.waitKey(1)