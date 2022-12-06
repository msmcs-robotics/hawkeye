import cv2
from predict import Predict_Centers
from colorama import Fore
from time import sleep
from turret import fire


# Load the cascade to compare frames to in order to detect faces
# Cascade Reference - https://github.com/adarsh1021/facedetection/blob/master/haarcascade_frontalface_default.xml
face_cascade = cv2.CascadeClassifier('./assets/haarcascade_frontalface_default.xml')

# Select the capture device. 0 -> /dev/video0
cap = cv2.VideoCapture(0)

# Try to set the resolution to 300x300 to save processing power
# However the resolution might be overriden by the camera driver
MAX_WIDTH = 500
MAX_HEIGHT = 500
cap.set(cv2.CAP_PROP_FRAME_WIDTH, MAX_WIDTH)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, MAX_HEIGHT)

# Delay between frames when tracking
between_tracked_frames = 0.01

def fancy_output(x, y, face_num_index):
    print(Fore.GREEN, 
        "Face #",Fore.RED,face_num_index+1, Fore.GREEN, "Detected at:",
        Fore.CYAN,
        x,
        Fore.WHITE,
        ":",
        Fore.YELLOW, 
        y)
    
def fancy_output_predict(x, y, face_num_index):
    print(Fore.GREEN, 
        "Face #",Fore.RED,face_num_index+1, Fore.GREEN, "Predicted at:",
        Fore.CYAN,
        x,
        Fore.WHITE,
        ":",
        Fore.YELLOW, 
        y)

def get_faces(frame):
    centersX = []
    centersY = []
    widths = []
    heights = []

        # Compare the image to the cascade
    faces = face_cascade.detectMultiScale(frame, 1.1, 4)
    
    # Loop through the detected faces if any
    # Keep track of the index for logs
    for idx, (x, y, w, h) in enumerate(faces):
        
        w2 = (w/100) * 50 # 50% of the width, place in center
        h2 = (h/100) * 35 # 30% of the height, place slightly above center

        centersX.append(int(x + w2))
        centersY.append(int(y + h2))
        widths.append(int(w))
        heights.append(int(h))
    
    return centersX, centersY, widths, heights

def get_frame():
    _, img = cap.read()
    # resize the frame to save processing power
    frame = cv2.resize(img, None, fx=1, fy=1, interpolation=cv2.INTER_AREA)
    # Convert to grayscale
    gray_frame = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    centersX, centersY, widths, heights = get_faces(gray_frame)

    return frame, centersX, centersY, widths, heights

while True:

    frame1, centersX_1, centersY_1 ,widths1, heights1 = get_frame()

    sleep(between_tracked_frames)

    frame2, centersX_2, centersY_2, widths2, heights2 = get_frame()

    new_centersX, new_centersY = Predict_Centers(widths1, widths2, heights1, heights2, centersX_1, centersY_1, centersX_2, centersY_2, MAX_WIDTH, MAX_HEIGHT).Track()


    # display the detected faces
    i = 0
    for center in range(len(centersX_2)):
        fancy_output(centersX_2[center], centersY_2[center], i)
        cv2.circle(frame2, (centersX_2[center], centersY_2[center]), 3, (0, 255, 0), 2)
        i += 1

    # display the predicted positions
    
    i = 0
    for center in range(len(new_centersX)):
        fancy_output_predict(new_centersX[center], new_centersY[center], i)
        cv2.circle(frame2, (new_centersX[center], new_centersY[center]), 3, (0, 0, 255), 2)
        fire(new_centersX[center], new_centersY[center])
        i += 1


    cv2.imshow('img', frame2)

    # predict the next location of the object
    #Track(centersX_1, centersY_1, centersX_2, centersY_2, MAX_HEIGHT, MAX_WIDTH)

    # Press 'ESC' to stop
    k = cv2.waitKey(30) & 0xff
    if k==27:
        break

cap.release()