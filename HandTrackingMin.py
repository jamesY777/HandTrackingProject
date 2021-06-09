import cv2
import mediapipe as mp
import time

cap = cv2.VideoCapture(0) #Create the video capture object

#Create hands object
mpHands = mp.solutions.hands
hands = mpHands.Hands() #Default static_image_mode=False; this is to detect and track the "hands"
mpDraw = mp.solutions.drawing_utils #This is built drawing function to draw dots/connections of the tracked hand landmarks (21 dots per hand)

#Recoding the FPS (frame per second)
pTime = 0 #previous time
cTime = 0 #current time


while True:
    sucess, img = cap.read()

    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB) #By default, cap.read() ussing cv2.VideoCapture is captureing BGR for color order; converting to RGB
    results = hands.process(imgRGB) #Process the hands from the image (video capture), the results are tracking the hands from video capture

    #print(results.multi_hand_landmarks) The can print out the tracked result of the hands
    if results.multi_hand_landmarks: #If hands detected
        for handLms in results.multi_hand_landmarks: #loop through hands landmark, the first layer handLms is one hand. There could be many hands captured.
            for id, lm in enumerate(handLms.landmark): #provide the list of landmarks in a tuple as (id, lm)
                #print(id, lm) #Each id is one of 21 dots for the hands from 0-20; For each of the dot, it contains landmark poisition x,y,z. X and Y are normorlized position, z is the depth (close of the camera)
                h, w, c = img.shape #Get the height, width of the image capture
                cx, cy = int(lm.x*w), int(lm.y*h) #Calculate the normolized position to pixel
                print(id, cx, cy) #Print the integer position of the landmark
                if id == 8: #highlight the finger tip of the index finger using a circle
                    cv2.circle(img, (cx, cy), 15, (255,0,255), cv2.FILLED) #argument https://www.geeksforgeeks.org/python-opencv-cv2-circle-method/

            mpDraw.draw_landmarks(img, handLms, mpHands.HAND_CONNECTIONS) #Drawing the dots/connections of hands landmark; need HAND_CONNECTIONS if drawing the connection

    cTime = time.time()
    fps = 1/(cTime-pTime)
    pTime = cTime

    cv2.putText(img, str(int(fps)), (10,70), cv2.FONT_HERSHEY_PLAIN, 3, color=(255,0,255), thickness=3) #Display the FPS on the screen, agruments at https://www.geeksforgeeks.org/python-opencv-cv2-puttext-method/

    cv2.imshow("Image", img)
    cv2.waitKey(1)