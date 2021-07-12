import cv2
import time
import numpy as np
import math
import HandTrackingModule as htm

#Pycaw use to adjust the audio volume
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
##########################
wCam, hCam = 640, 480
##########################

cap = cv2.VideoCapture(0)
cap.set(3, wCam)
cap.set(4, hCam)
pTime = 0

devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))
# volume.GetMute()
# volume.GetMasterVolumeLevel()
volRange = volume.GetVolumeRange() #volume range is -64 to 0

detector = htm.handDetector(detectionCon=0.7)

vol = 0
volBar = 400
volPct = 0
while True:
    success, img = cap.read()
    
    img = detector.findHands(img)
    lmList = detector.findPosition(img, draw = False)
    if len(lmList) != 0:
        #print(lmList)
        x1, y1 = lmList[4][1], lmList[4][2] #thumb tip
        x2, y2 = lmList[8][1], lmList[8][2] #index finger tip

        cx, cy = (x1 + x2) // 2, (y1 + y2) // 2

        length = math.hypot(x2-x1, y2-y1)

        cv2.circle(img, (x1, y1), 5, (255,0,255), cv2.FILLED)
        cv2.circle(img, (x2, y2), 5, (255,0,255), cv2.FILLED)
        cv2.line(img, (x1,y1), (x2,y2), (255,00,255), 3)
        cv2.circle(img, (cx, cy), 5, (255,0,255), cv2.FILLED)

        #print(length) #check the range of between two fingers which is 13 to 150

        # Volume Range -64 - 0
        vol = np.interp(length, [13, 150], [-60, -10]) #Map one range to another range using np
        volume.SetMasterVolumeLevel(vol, None)

        #To set volume legend bar on the side
        volBar = np.interp(length, [13, 150], [400, 150])
        volPct = np.interp(length, [13, 150], [0, 100])

    #Show the percentage as a bar
    cv2.rectangle(img, (50,150), (85,400), (247,121,4), 1)
    cv2.rectangle(img, (50,int(volBar)), (85,400), (247,121,4), cv2.FILLED)
    #Show the volume percentage value
    cv2.putText(img, f'{int(volPct)}%', (40,450), cv2.FONT_HERSHEY_COMPLEX, 1, (247,121,4), 1)

    cTime = time.time()
    fps = 1/(cTime-pTime)
    pTime = cTime

    cv2.putText(img, f'FPS: {int(fps)}', (40,70), cv2.FONT_HERSHEY_COMPLEX, 1, (255,0,0), 1)
    
    cv2.imshow("Img", img)
    cv2.waitKey(1)