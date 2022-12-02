from imutils.video import VideoStream
import argparse
import datetime
import imutils
import time
import cv2
import numpy as np
from time import sleep
from colorama import Fore

cap = VideoStream(src=0).start()
time.sleep(2.0)

MAX_WIDTH = 500
MAX_HEIGHT = 500

min_target_area = ((MAX_WIDTH * MAX_HEIGHT) / 100) * 3
max_target_area = ((MAX_WIDTH * MAX_HEIGHT) / 100) * 25

# initialize the first frame in the video stream
firstFrame = None
secFrame = None
delay_between_frames = 0.01

def fancy_output(x, y, face_num_index, action):
	print(
		Fore.GREEN, "Obj #",
		Fore.RED, face_num_index+1, 
		Fore.GREEN, "{} at:".format(action), 
		Fore.CYAN, x,
        Fore.WHITE, ":",
        Fore.YELLOW, y
		)

def gray_blur(frame):
	frame = imutils.resize(frame, width=MAX_WIDTH)
	grayframe = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
	grayframe = cv2.GaussianBlur(grayframe, (21, 21), 0)
	return grayframe

def get_contours(grayframe, frameid):
	frameDelta = cv2.absdiff(frameid, grayframe)
	thresh = cv2.threshold(frameDelta, 25, 255, cv2.THRESH_BINARY)[1]
	thresh = cv2.dilate(thresh, None, iterations=2)
	cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,
		cv2.CHAIN_APPROX_SIMPLE)
	cnts = imutils.grab_contours(cnts)
	return cnts

def check_target_size(w, h):
	target_area = w * h
	if target_area < min_target_area:
		return False
	elif target_area > max_target_area:
		return False
	else:
		return True

def check_out_of_frame(x, y):
	if x > MAX_WIDTH:
			x = MAX_WIDTH
	elif x < 0:
		x = 0
	if y > MAX_HEIGHT:
		y = MAX_HEIGHT
	elif y < 0:
		y = 0

	return x, y

def calc_3rd_center(x1, y1, x2, y2):
	# convert to vectors
	r1 = np.array([x1, y1])
	r2 = np.array([x2, y2])

	# get delta r
	delta_r = r2 - r1

	# make a new vector
	r3 = r2 + delta_r

	# get the x and y coordinates of the new vector
	x = r3[0]
	y = r3[1]

	# check if coordinates are out of frame
	x, y = check_out_of_frame(x, y)

	return x, y


while True:

	cX1 = []
	cY1 = []
	cX2 = []
	cY2 = []

	widths1 = []
	heights1 = []
	widths2 = []
	heights2 = []

	frame1 = cap.read()
	sleep(delay_between_frames)
	frame2 = cap.read()

	# get contours from 1st frame
	if frame1 is None:
		break
	frame1_gray = gray_blur(frame1)
	if firstFrame is None:
		firstFrame = frame1_gray
		continue
	cnts1 = get_contours(frame1_gray, firstFrame)
	
	
	# get contours from 2nd frame
	frame2_gray = gray_blur(frame2)
	if secFrame is None:
		secFrame = frame2_gray
		continue
	cnts2 = get_contours(frame2_gray, secFrame)

	for c in cnts1:
		(x, y, w, h) = cv2.boundingRect(c)
		if check_target_size(w, h):
			#cv2.rectangle(frame1, (x, y), (x + w, y + h), (0, 255, 0), 2)
			cx = int(x+w/2)
			cy = int(y+h/2)
			cX1.append(int(cx))
			cY1.append(int(cy))
			widths1.append(w)
			heights1.append(h)
			#cv2.circle(frame1, (cx, cy), 3, (0, 255, 0), 3)
	
	for c in cnts2:
		(x, y, w, h) = cv2.boundingRect(c)
		if check_target_size(w, h):
			cv2.rectangle(frame2, (x, y), (x + w, y + h), (0, 255, 0), 2)
			cx = int(x+w/2)
			cy = int(y+h/2)
			cX2.append(int(cx))
			cY2.append(int(cy))
			widths2.append(w)
			heights2.append(h)
			#cv2.circle(frame2, (cx, cy), 3, (0, 255, 0), 3)

	for i in range(0, len(cX2)):
		try:
			fancy_output(cX2[i], cY2[i], i+1, "Detected at: ")
			cv2.circle(frame2, (int(cX2[i]), int(cY2[i])), 3, (0, 255, 0), 3)
		except:
			pass

	for i in range(len(cX2)):
		try:
			nx, ny = calc_3rd_center(cX1[i], cY1[i], cX2[i], cY2[i])
			fancy_output(nx, ny, i+1, "Predicted at: ")
			cv2.circle(frame2, (int(nx), int(ny)), 3, (0, 0, 255), 3)
		except:
			pass

	cv2.imshow("Result", frame1)
	cv2.imshow("Result2", frame2)
	key = cv2.waitKey(1) & 0xFF
	# if the `q` key is pressed, break from the lop
	if key == ord("q"):
		break
# cleanup the camera and close any open windows
cap.stop()
cv2.destroyAllWindows()