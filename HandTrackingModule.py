"""
James Yan - June 08, 2021 
Creating a class that can be reusable from other project quickly that using the Handtracking tech.
The class will creat mp.Hands.Hands object that can process a image or stream image and detect the Hands from the image.
The class wiil create mp.Draw object which will draw the dots/connection on the detected hands within the images.
"""

import cv2
import mediapipe as mp
import time
import math

class handDetector():
    def __init__(self, mode=False, maxHands=1, detectionCon=0.5, trackCon=0.5 ):
        self.mode = mode
        self.maxHands = maxHands
        self.detectionCon = detectionCon
        self.trackCon = trackCon
        
        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands(self.mode, self.maxHands, self.detectionCon, self.trackCon) #Default static_image_mode=False; this is to detect and track the "hands"
        self.mpDraw = mp.solutions.drawing_utils #This is built drawing function to draw dots/connections of the tracked hand landmarks (21 dots per hand)
        self.drawSpec_dots = self.mpDraw.DrawingSpec(thickness=1, circle_radius=1, color=(226,241,56)) #Specify the draw style
        self.drawSpec_line = self.mpDraw.DrawingSpec(thickness=2, color=(223,93,3))

        self.tipIds = [4,8,12,16,20]
    #The function detected the hands and return the image with dots/connections draw on the hands
    def findHands(self, img, draw=True):
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB) #By default, cap.read() ussing cv2.VideoCapture is captureing BGR for color order; converting to RGB
         
        #Process the hands from the image (video capture), the results are tracking the hands from video capture
        #Make result a var with in the self, so it can be used again.
        self.results = self.hands.process(imgRGB)
        #print(results.multi_hand_landmarks) The can print out the tracked result of the hands
        if self.results.multi_hand_landmarks: #If hands detected
            for handLms in self.results.multi_hand_landmarks: #loop through hands landmark, the first layer handLms is one hand. There could be many hands captured.
                if draw:
                    self.mpDraw.draw_landmarks(img, handLms, self.mpHands.HAND_CONNECTIONS, self.drawSpec_dots,connection_drawing_spec = self.drawSpec_line) #Drawing the dots/connections of hands landmark; need HAND_CONNECTIONS if drawing the connection
                    #Overwrite dots on all hands
                    for lm in handLms.landmark: 
                        h, w, c = img.shape #Get the height, width of the image capture
                        cx, cy = int(lm.x*w), int(lm.y*h) #Calculate the normolized position to pixel
                        cv2.circle(img, (cx,cy), 2, (226,241,56), cv2.FILLED) 
        return img

    # A function to return the position of the Hands within the image
    def findPosition(self, img, handNo=0, draw=True):
        self.lmList = []
        if self.results.multi_hand_landmarks:
            myHand = self.results.multi_hand_landmarks[handNo]
            for id, lm in enumerate(myHand.landmark): #provide the list of landmarks in a tuple as (id, lm)
                    #print(id, lm) #Each id is one of 21 dots for the hands from 0-20; For each of the dot, it contains landmark poisition x,y,z. X and Y are normorlized position, z is the depth (close of the camera)
                    h, w, c = img.shape #Get the height, width of the image capture
                    cx, cy = int(lm.x*w), int(lm.y*h) #Calculate the normolized position to pixel
                    self.lmList.append([id, cx, cy])
                    if draw: #and id == 8: #highlight the finger tip of the index finger using a circle
                        cv2.circle(img, (cx, cy), 3, (226,241,56), cv2.FILLED) #argument https://www.geeksforgeeks.org/python-opencv-cv2-circle-method/
        return self.lmList

    # A function returns a list with indicotr of 5 finger tips
    def fingersUp(self):
        fingers = []
        # Calculate the distance of two dots on the hands, by default is the distance to wrist
        def lenCal(id, ref=0):
                x, y = self.lmList[id][1], self.lmList[id][2]
                xref, yref = self.lmList[ref][1], self.lmList[ref][2]
                length = math.hypot(x-xref, y-yref)
                return length
        # Append thumb indicator 
        thumb_indicator = lenCal(4,17) > lenCal(2,17)
        fingers.append(thumb_indicator)
        # Append the other fingers(except tips indicator
        for id in self.tipIds[1:]:
            indicator = lenCal(id) > lenCal(id-2)
            fingers.append(indicator)
        return fingers

# A main() function that can be run itself.
def main():

    cap = cv2.VideoCapture(0) #Create the video capture object
    
    pTime = 0 #previous time
    cTime = 0 #current time
    
    detector = handDetector() #Create the detector object based on the class above
    
    while True:
        sucess, img = cap.read()

        img = detector.findHands(img)
        lmList = detector.findPosition(img)
        if len(lmList) !=0: #In case the hand is not showing in the video yet
            print(lmList[8])
        cTime = time.time()

        fps = 1/(cTime-pTime)
        pTime = cTime

        cv2.putText(img, str(int(fps)), (10,70), cv2.FONT_HERSHEY_PLAIN, 3, color=(255,0,0), thickness=1) #Display the FPS on the screen, agruments at https://www.geeksforgeeks.org/python-opencv-cv2-puttext-method/

        cv2.imshow("Image", img)
        cv2.waitKey(1)
if __name__ == "__main__":
    main()