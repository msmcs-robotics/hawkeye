from math import degrees
from auxillary import Pi_Turret, Arduino_Turret
from auxillary import Alarm

import cv2
from scipy.interpolate import interp1d as map
from colorama import Fore

# Debug
# True - only try to detect faces
# False - detect faces, and send coordinates to Arduino 
debug = True

# Turret Type
# True - Pi Turret
# False - Arduino Turret
pi_turret = True

# Resolution
CAP_WIDTH = 640
CAP_HEIGHT = 480
# The servo's range of motion is n-degrees larger than the camera's field of view
# Say the camera's field of view is 60-degrees, and the servo's range of motion is 180-degrees
# 180 minus 60 and then divide by 2 because the camera's field of view is centered on the servo
CAP_WIDTH_VIEW_ERR = 60 # horizontal field of view
CAP_HEIGHT_VIEW_ERR = 60 # vertical field of view
cap = cv2.VideoCapture(0)

class Hawkeye:

    # Eventually Convert the coordinates to duty cycles
    def to_duty_cycle(x, y):
        # Convert pixel coordinates to degrees
        x = map([0, CAP_WIDTH], [0, 180])
        y = map([0, CAP_HEIGHT], [0, 180])
        # Compensate for the camera's field of view
        
        # Horizontal Axis
        if x > CAP_WIDTH_VIEW_ERR and x < CAP_WIDTH - CAP_WIDTH_VIEW_ERR:
            pass
        elif x < CAP_WIDTH_VIEW_ERR:
            x = x + CAP_WIDTH_VIEW_ERR
        elif x > CAP_WIDTH - CAP_WIDTH_VIEW_ERR:
            x = x - CAP_WIDTH_VIEW_ERR
        
        # Vertical Axis
        if y > CAP_HEIGHT_VIEW_ERR and y < CAP_HEIGHT - CAP_HEIGHT_VIEW_ERR:
            pass
        elif y < CAP_HEIGHT_VIEW_ERR:
            y = y + CAP_HEIGHT_VIEW_ERR
        elif y > CAP_HEIGHT - CAP_HEIGHT_VIEW_ERR:
            y = y - CAP_HEIGHT_VIEW_ERR

        # Convert degrees to duty cycle
        x = (x/18) + 2.5
        y = (y/18) + 2.5
        return x, y

    # The main loop
    def start():
        num_faces, centersX, centersY = Hawkeye.detect_faces()
        
        for face in range(num_faces):
            Alarm.sound_alarm()

        for center in range(num_faces):
            #print(Fore.BLUE + "Face Detected: " + Fore.GREEN + "{}, {}".format(centersX[center], centersY[center]))
            if pi_turret:
                Pi_Turret.fire(centersX[center], centersY[center])
            else:
                Arduino_Turret.fire(centersX[center], centersY[center])

    # Detect faces
    # Cascade Reference - https://github.com/adarsh1021/facedetection/blob/master/haarcascade_frontalface_default.xml
    def detect_faces():

        face_cascade = cv2.CascadeClassifier('./assets/haarcascade_frontalface_default.xml')
        _, img = cap.read()
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.1, 4)
        
        centersX = []
        centersY = []
        for (x, y, w, h) in faces:
            w = (w/100) * 50 # 50% of the width, centered
            h = (h/100) * 35 # 35% of the height, slightly above the center of the face

            #cv2.circle(img, (int(x + w), int(y + h)), 5, (0, 0, 255), 2) # Reduce CPU load
            #print(Fore.CYAN + x+w, " : ", Fore.YELLOW + y+h)
            
            # Do math so servo can understand
            x, y = Hawkeye.to_duty_cycle(x, y)
            centersX.append(x)
            centersY.append(y)
        
        #cv2.imshow('img', img) # Reduce CPU load
        return len(faces), centersX, centersY

while True:
    if not debug:
        Hawkeye.start()
    else:
        Hawkeye.detect_faces()
    k = cv2.waitKey(30) & 0xff
    # Press 'ESC' to quit
    if k==27:
        break
    cap.release()