import cv2
from colorama import Fore

# Load the cascade to compare frames to in order to detect faces
# Cascade Reference - https://github.com/adarsh1021/facedetection/blob/master/haarcascade_frontalface_default.xml
face_cascade = cv2.CascadeClassifier('./assets/haarcascade_frontalface_default.xml')

# Select the capture device. 0 -> /dev/video0
cap = cv2.VideoCapture(0, cv2.CAP_V4L2)

# Try to set the resolution to 500x500 to save processing power
# However the resolution might be overriden by the camera driver
MAX_WIDTH = 500
MAX_HEIGHT = 500
cap.set(cv2.CAP_PROP_FRAME_WIDTH, MAX_WIDTH)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, MAX_HEIGHT)

def fancy_output(x, y, face_num_index):
    print(Fore.GREEN, 
        "Face #",Fore.RED,face_num_index+1, Fore.GREEN, "Detected at:",
        Fore.CYAN,
        x,
        Fore.WHITE,
        ":",
        Fore.YELLOW, 
        y)

while True:

    # Capture frame-by-frame
    _, img = cap.read()
    
    # resize the frame to save processing power
    img = cv2.resize(img, None, fx=1, fy=1, interpolation=cv2.INTER_AREA)
    
    # Convert to grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    # Compare the image to the cascade
    faces = face_cascade.detectMultiScale(gray, 1.1, 4)
    
    # Loop through the detected faces if any
    # Keep track of the index for logs
    for idx, (x, y, w, h) in enumerate(faces):
        
        #w = (w/100) * 50 # 50% of the width, place in center
        #h = (h/100) * 35 # 30% of the height, place slightly above center
        
        # Draw a rectangle around the face
        cv2.rectangle(img, (x, y), (x+w, y+h), (255, 0, 0), 2)
    
    # Display a window with the image
    cv2.imshow('img', img)

    # Press 'ESC' to stop
    k = cv2.waitKey(30) & 0xff
    if k==27:
        break

cap.release()