import cv2
from colorama import Fore
#from aux import *

bird1_cascade = cv2.CascadeClassifier('assets/bird1-cascade.xml')
bird2_cascade = cv2.CascadeClassifier('assets/bird2-cascade.xml')
 
cap = cv2.VideoCapture('assets/test-2.mp4')

# Resolution
CAP_WIDTH = 300
CAP_HEIGHT = 300
# The servo's range of motion is n-degrees larger than the camera's field of view
# Say the camera's field of view is 60-degrees, and the servo's range of motion is 180-degrees
# 180 minus 60 and then divide by 2 because the camera's field of view is centered on the servo
CAP_WIDTH_VIEW_ERR = 60 # horizontal field of view
CAP_HEIGHT_VIEW_ERR = 60 # vertical field of view

def fancy_output(x, y, bird_num_index, bird_type):
    print(
        Fore.GREEN, "Bird ({}) #".format(bird_type),
        Fore.RED, bird_num_index+1,
        Fore.GREEN, "Detected at:",
        Fore.CYAN, x,
        Fore.WHITE, ":",
        Fore.YELLOW, y)


while 1: 
 
    ret, img = cap.read() 
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    birds1 = bird1_cascade.detectMultiScale(gray, 1.3, 5)
    birds2 = bird2_cascade.detectMultiScale(gray, 1.3, 5)
    
    for bird, (x, y, w, h) in enumerate(birds1):
        
        w = (w/100) * 50 # 50% of the width, place in center
        h = (h/100) * 35 # 30% of the height, place slightly above center
        
        # Draw a red dot on the face
        cv2.circle(img, (int(x + w), int(y + h)), 3, (0, 0, 255), 2)
        # Fancy output to terminal
        fancy_output(x+w, y+h, bird, "1")
        
        #Turret.run(x+w, y+h, CAP_WIDTH, CAP_HEIGHT, CAP_WIDTH_VIEW_ERR, CAP_HEIGHT_VIEW_ERR)

    
    # Display a window with the image
    cv2.imshow('img', img)

    for bird, (x, y, w, h) in enumerate(birds2):
        
        w = (w/100) * 50 # 50% of the width, place in center
        h = (h/100) * 50 # 30% of the height, place slightly above center
        
        # Draw a red dot on the face
        cv2.circle(img, (int(x + w), int(y + h)), 3, (0, 0, 255), 2)
        # Fancy output to terminal
        fancy_output(x+w, y+h, bird, "2")
    
    # Display a window with the image
    cv2.imshow('img', img)
 
    k = cv2.waitKey(30) & 0xff
    if k == 27:
        break
 
cap.release()

cv2.destroyAllWindows() 
