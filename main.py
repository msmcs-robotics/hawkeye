import math
import cv2
from time import sleep



# if objects are too close to each other, they are considered the same object 
dist_btw_objs_thresh = 50

# Create the background subtractor
hist_size = 10
subtractor_threshold = 50
subtractor_detect_shadows = False
subtractor = cv2.createBackgroundSubtractorMOG2(history=hist_size, varThreshold=subtractor_threshold, detectShadows=subtractor_detect_shadows)

# Camera settings
cap = cv2.VideoCapture(0)
time_between_frames = 0.01
MAX_WIDTH = 500
MAX_HEIGHT = 500
cap.set(cv2.CAP_PROP_FRAME_WIDTH, MAX_WIDTH)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, MAX_HEIGHT)

def get_frame():
    _, frame = cap.read()

    new_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    mask = subtractor.apply(frame)

    new_frame = cv2.blur(mask, (5,5))

    minVal, maxVal, minLoc, maxLoc = cv2.minMaxLoc(new_frame)
    ret,new_frame = cv2.threshold(new_frame, 0.3*maxVal, 255, cv2.THRESH_BINARY)
    median = cv2.medianBlur(new_frame, 7)

    se = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(11, 11))
    new_frame = cv2.morphologyEx(new_frame, cv2.MORPH_DILATE, se)
    new_frame = cv2.morphologyEx(new_frame, cv2.MORPH_CLOSE, se)

    contours, hierarchy = cv2.findContours(new_frame,cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE)

    x = []

    for contour in contours:
        x.append(len(contour))
    m = max(x)
    p = [i for i, j in enumerate(x) if j == m]

    x, y, w, h = cv2.boundingRect(contours[p[0]])

    return x, y, w, h, frame

def check_dist_thresh(x1, x2, y1, y2):
    dist = math.sqrt((x2 - x1)**2 + (y2 - y1)**2)
    if dist < dist_btw_objs_thresh:
        return False
    else:
        return True

while True:  

    try:
        x1, y1, w1, h1, frame1 = get_frame()
        sleep(time_between_frames)
        x2, y2, w2, h2, frame2 = get_frame()

        # if object is not large enough, skip
        if w1 < 50 or h1 < 50:
            obj1 = False
        else:
            obj1 = True

        if w2 < 50 or h2 < 50:
            obj2 = False
        else:
            obj2 = True

        if obj1 and obj2:
            if check_dist_thresh(x1, x2, y1, y2):
                print("multiple objects")
                cv2.rectangle(frame1, (x1, y1), (x1 + w1, y1 + h1), (0, 255, 0), 2)
                cv2.rectangle(frame2, (x2, y2), (x2 + w2, y2 + h2), (255, 0, 0), 2)
            else:
                print("same object")
                cv2.rectangle(frame1, (x1, y1), (x1 + w1, y1 + h1), (0, 255, 0), 2)
        else:
            print("no objects (rel)")

        cv2.imshow("frame1", frame1)
        cv2.imshow("frame2", frame2)

    except:
        print("no objects (abs)")

    key = cv2.waitKey(30)  
    if key == 27:  
        break
cap.release()  
cv2.destroyWindowKey()  