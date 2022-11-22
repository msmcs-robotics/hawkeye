import numpy as np
import cv2
from colorama import Fore

def fancy_depth_predict(x, y, face_num_index):
    print(Fore.GREEN, 
        "Face #",Fore.RED,face_num_index+1, Fore.GREEN, "Depth at:",
        Fore.CYAN,
        x,
        Fore.WHITE,
        ":",
        Fore.YELLOW, 
        y)
class Predict_Centers:

    def __init__(self, widths1, widths2, heights1, heights2, x_centers1, y_centers1, x_centers2, y_centers2, max_width, max_height):
        
        self.pos1_vecs = []
        self.pos2_vecs = []

        self.widths1 = widths1
        self.widths2 = widths2

        self.heights1 = heights1
        self.heights2 = heights2
        
        self.x_centers1 = x_centers1
        self.y_centers1 = y_centers1

        self.x_centers2 = x_centers2
        self.y_centers2 = y_centers2

        self.vec_centersX = []
        self.vec_centersY = []

        self.dep_centersX = []
        self.dep_centersY = []

        self.max_height = max_height
        self.max_width = max_width

    def check_out_of_frame(self, x, y):
        if x > self.max_width:
            x = self.max_width
        if x < 0:
            x = 0
        if y > self.max_height:
            y = self.max_height
        if y < 0:
            y = 0

        return x, y

    def depth_perception(self, x, y, w1, w2, h1, h2):

        delta_w = w2 - w1
        delta_h = h2 - h1

        # avg change in size
        ratio = (delta_w + delta_h) / 2
        ratio = round((ratio / 100), 2)

        # if ratio is greater than 1, the object is getting closer
        # if ratio is less than 1, the object is getting further away
        # if ratio is equal to 1, the object is not moving

        # therefore

        # if ratio is greater than 1, we want to aim closer to the object
        # if ratio is less than 1, we want to aim further away from the object
        # if ratio is equal to 1, we want to aim at the same distance as the object
        xneg = False
        if x < 0:
            xneg = True

        # if aiming closer to the object, subtract value from x_center
        if ratio > 1:
            x3 = abs(x) - (abs(x) * ratio)
        # if aiming further away from the object, add value to x_center
        elif ratio < 1:
            x3 = abs(x) + (abs(x) * ratio)
        # if ratio is equal to 1, aim at the same distance as the object
        else:
            x3 = x
        # check negative
        if xneg == True:
            x3 = x3 * -1
        
        yneg = False
        if y < 0:
            yneg = True
        # if aiming closer to the object, subtract value from y_center
        if ratio > 1:
            y3 = abs(y) - (abs(y) * ratio)
        # if aiming further away from the object, add value to y_center
        if ratio < 1:
            y3 = abs(y) + (abs(y) * ratio)
        # if ratio is equal to 1, aim at the same distance as the object
        else:
            y3 = y
        # check negative
        if yneg == True:
            y3 = y3 * -1

        x3, y3 = self.check_out_of_frame(x3, y3)

        self.dep_centersX.append(x3)
        self.dep_centersY.append(y3)

    def calc_r3(self, r1, r2):

        # get delta r
        delta_r = r2 - r1

        # make a new vector
        r3 = r2 + delta_r

        # get the x and y coordinates
        x = r3[0]
        y = r3[1]

        # check if the new position is within the frame, if not, set it to the edge of the frame
        x, y = self.check_out_of_frame(x, y)
        
        self.vec_centersX.append(x)
        self.vec_centersY.append(y)

    def Track(self):
        
        # create a vector for each position
        for i in range(len(self.x_centers1)):
            # convert the x and y coordinates to a vector
            try:
                pos1_vec = np.array([self.x_centers1[i], self.y_centers1[i]])
                pos2_vec = np.array([self.x_centers2[i], self.y_centers2[i]])

                self.pos1_vecs.append(pos1_vec)
                self.pos2_vecs.append(pos2_vec)
            except:
                print("Error: no vector could be created")
                pass

        # calculate the next position as vector
        # then convert it to x and y coordinates
        #print("number of vecs:" + str(len(self.pos1_vecs)))
        
        c = 0

        for i in range(len(self.pos1_vecs)):
            self.calc_r3(self.pos1_vecs[i], self.pos2_vecs[i])
        
        #print("number of vec centers:" + str(len(self.vec_centersX)))

        for i in range(len(self.vec_centersX)):
            self.depth_perception(self.vec_centersX[i], self.vec_centersY[i], self.widths1[i], self.widths2[i], self.heights1[i], self.heights2[i])
            fancy_depth_predict(self.dep_centersX[i], self.dep_centersY[i], i)
        
        #print("number of dep centers:" + str(len(self.dep_centersX)))
        return self.vec_centersX, self.vec_centersY

        #return self.dep_centersX, self.dep_centersY