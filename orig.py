from imutils.video import VideoStream
import argparse
import datetime
import imutils
import time
import cv2

cap = VideoStream(src=0).start()
time.sleep(2.0)

# initialize the first frame in the video stream
firstFrame = None

# loop over the frames of the video
while True:

    frame = cap.read()
    text = "Unoccupied"


    if frame is None:
        break

    frame = imutils.resize(frame, width=500)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (21, 21), 0)


    if firstFrame is None:
        firstFrame = gray
        continue


    frameDelta = cv2.absdiff(firstFrame, gray)
    thresh = cv2.threshold(frameDelta, 25, 255, cv2.THRESH_BINARY)[1]
    thresh = cv2.dilate(thresh, None, iterations=2)
    cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,
        cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)

    for c in cnts:
        (x, y, w, h) = cv2.boundingRect(c)
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
        cx = int(x+w/2)
        cy = int(y+h/2)
        cv2.circle(frame, (cx, cy), 3, (0,0,255), 3)


    cv2.imshow("Security Feed", frame)
    cv2.imshow("Thresh", thresh)
    cv2.imshow("Frame Delta", frameDelta)
    key = cv2.waitKey(1) & 0xFF
    # if the `q` key is pressed, break from the lop
    if key == ord("q"):
        break
# cleanup the camera and close any open windows
cap.stop()
cv2.destroyAllWindows()