import cv2
from time import sleep

cap = cv2.VideoCapture(0)

MAX_WIDTH = 500
MAX_HEIGHT = 500

hist_size = 10
subtractor_threshold = 90
subtractor_detect_shadows = False


subtractor = cv2.createBackgroundSubtractorMOG2(history=hist_size, varThreshold=subtractor_threshold, detectShadows=subtractor_detect_shadows)

cap.set(cv2.CAP_PROP_FRAME_WIDTH, MAX_WIDTH)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, MAX_HEIGHT)


def target_tuning(x, y, w, h):
    #w += 10
    #h += 10

    # threshold for size of object?
    if w <= 20 or h <= 20:
        pass
    else:
        x, y, w, h = x, y, w, h
        
    return x, y, w, h

while True:  
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

    try:
        for contour in contours:
            x.append(len(contour))
        m = max(x)
        p = [i for i, j in enumerate(x) if j == m]

        x, y, w, h = cv2.boundingRect(contours[p[0]])

        x, y, w, h = target_tuning(x, y, w, h)
        
        color = (0, 0, 255)

        cv2.rectangle(frame, (x,y),(x+w,y+h),color, 3)
        cv2.imshow("result", frame)

    except:
        #print("Nothing Found...")
        pass

    key = cv2.waitKey(30)  
    if key == 27:  
        break
cap.release()  
cv2.destroyWindowKey()  