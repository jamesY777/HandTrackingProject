## Hand Tracking
### Summary
The script below is based on python package *mediapipe==0.8.5* - Hand Tracking. The model can track the hand object that captured in the image/vedio object.

The mdeiapipe hand tracking return the hand object in 21 dots, displaying below:
![](/image/hand_landmarks.png)

### For quick start
Use the *HandTrackingMin.py*. The script will use the first camera device to track any Hand captured in the camera. Additionally, it also highlights the index finger (with id=8) in this quick start-up.

![](/image/hand_min.PNG)

### HandTrackingModule
*HandTrackingModule.py* defines the main class that can be reused in other applications. The class name is *handDetector*, it contains a few basic methods. This script can also be called itself which will perform the same function as *HandTrackingMin.py*. In addition, added a little cutomized color for land mark and dots.

![](/image/hand_module.PNG)

To test loading the module and use the class, check the *Test_HandTracking.py*

### Appication 1 - Finger Counting
*fingerCounting.py* is a simple application that calculte the number of fingers based on captured hands.
In the module class, method *fingerUp* comparing the length between tip-to-wrist VS pip-to-wrist; for thumb, comparing tip-to-pinky_mcp vs thumb_mpc-to-pinky_mcp, and return a list with 1-finger up, 0-finger down.
The appliction displays the # of fingers that is up.

![](/image/finger_count.PNG)

### Application 2 - painter
*painter.py* is a painter application (sorry about my UI design).
This is an extend of finger counting application, where 2-finger up to "pick color" and 1-finger up to draw a picture on the screen.

*Note: There is no save function.*

![](/image/painter.PNG)

### Application 3 - volume Control
*volumeControl.py* is simple function to control the sound volume using thumb_tip-to-index_finger_tip. The MAX volume is mapped to 50% (to avoid too_load situation during test).

![](/image/volumeControl.PNG)

### Reference - meidapipe package
Source: https://google.github.io/mediapipe/solutions/hands.html

Thanks to free training video: https://www.youtube.com/watch?v=01sAkU_NvOY