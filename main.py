
from imutils.video import VideoStream
import argparse
import datetime
import imutils
from time import sleep
import cv2
from predict import Predict_Centers

# recommended to move out of the way of the camera
delay = 3
for i in range(0, delay):
	print(delay - i)
	sleep(1)

# camera settings
cap = VideoStream(src=0).start()
MAX_WIDTH = 500
MAX_HEIGHT = 500

# misc global variables
firstFrame = None
delay_btw_frames = 0.01


# max area size is 1/4 of the screen
obj_max_area_size = (MAX_WIDTH * MAX_HEIGHT) / 4
# min area size is 1/100 of the screen
obj_min_area_size = (MAX_WIDTH * MAX_HEIGHT) / 100

# or just hard coded pixel values
#obj_max_area_size = 40000
#obj_min_area_size = 1000

def get_objs():
	
	frame = cap.read()
	frame = imutils.resize(frame, width=MAX_WIDTH, height=MAX_HEIGHT)
	gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
	gray = cv2.GaussianBlur(gray, (21, 21), 0)

	return frame, gray

def get_contours(gray):
	frameDelta = cv2.absdiff(firstFrame, gray)
	thresh = cv2.threshold(frameDelta, 25, 255, cv2.THRESH_BINARY)[1]
	thresh = cv2.dilate(thresh, None, iterations=2)
	cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,
		cv2.CHAIN_APPROX_SIMPLE)
	cnts = imutils.grab_contours(cnts)
	return cnts

def target_tune(contours):
	# return x and y coordinates of centers of contours
	centers_x = []
	centers_y = []
	widths = []
	heights = []

	for c in contours:
		(x, y, w, h) = cv2.boundingRect(c)
		# if rectangle is too small or to large, ignore it
		if not (w * h < obj_min_area_size) or (w * h > obj_max_area_size):
			for c2 in contours:
				(x2, y2, w2, h2) = cv2.boundingRect(c2)
				if not (x > x2 and y > y2 and x + w < x2 + w2 and y + h < y2 + h2):
					centers_x.append(x + w / 2)
					centers_y.append(y + h / 2)
	
	return centers_x, centers_y, widths, heights

while True:

	centersX1 = []
	centersY1 = []

	centersX2 = []
	centersY2 = []

	frame1, gray1 = get_objs()
	if firstFrame is None:
		firstFrame = gray1
	contours1 = get_contours(gray1)

	sleep(delay_btw_frames)

	frame2, gray2 = get_objs()
	contours2 = get_contours(gray2)

	centersX1, centersY1, widths1, heights1 = target_tune(contours1)
	centersX2, centersY2, widths2, heights2 = target_tune(contours2)

	'''for i in range(0, len(centersX1)):
		try:
			cv2.circle(frame1, (int(centersX1[i]), int(centersY1[i])), 5, (0, 0, 255), 3)
			cv2.circle(frame2, (int(centersX2[i]), int(centersY2[i])), 5, (0, 0, 255), 3)
		except:
			pass'''

	#new_centersX, new_centersY = Predict_Centers(widths1, widths2, heights1, heights2, centersX1, centersY1, centersX2, centersY2, MAX_WIDTH, MAX_HEIGHT).Track()

	# show old centers
	for i in range(0, len(centersX1)):
		try:
			cv2.circle(frame1, (int(centersX1[i]), int(centersY1[i])), 5, (0, 255, 0), 3)
		except:
			pass
	
	# show new centers
	#for i in range(0, len(new_centersX)):
	#	cv2.circle(frame1, (int(new_centersX[i]), int(new_centersY[i])), 5, (0, 0, 255), 3)

	cv2.imshow("Result", frame1)
	#cv2.imshow("Thresh", thresh)
	#cv2.imshow("Frame Delta", frameDelta)
	
	key = cv2.waitKey(1) & 0xFF
	if key == 27:
		break


cap.stop()
cv2.destroyAllWindows()