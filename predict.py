import numpy as np
import cv2

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

    def depth_perception(self, x1, x2, y1, y2, w1, w2, h1, h2):
        
        ratio = (w1/w2)

        if ratio > 1:
            ratio = -ratio

        # the increase of the distance between the two points
        delta_x = x2 - x1
        delta_y = y2 - y1

        # multiply the increase with the ratio
        delta_x = delta_x * ratio
        delta_y = delta_y * ratio

        # add the increase to the second point
        x3 = x2 + delta_x
        y3 = y2 + delta_y

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
            pos1_vec = np.array([self.x_centers1[i], self.y_centers1[i]])
            pos2_vec = np.array([self.x_centers2[i], self.y_centers2[i]])

            self.pos1_vecs.append(pos1_vec)
            self.pos2_vecs.append(pos2_vec)
        
        # calculate the next position as vector
        # then convert it to x and y coordinates
        print("number of vecs:" + str(len(self.pos1_vecs)))
        
        c = 0

        for i in range(len(self.pos1_vecs)):
            self.calc_r3(self.pos1_vecs[i], self.pos2_vecs[i])
        
        #for i in range(len(self.vec_centersX)):
            #self.depth_perception(self.vec_centersX[i], self.dep_centersX[i], self.vec_centersY[i], self.dep_centersY[i], self.widths1[i], self.widths2[i], self.heights1[i], self.heights2[i])
        
        return self.vec_centersX, self.vec_centersY

        #return self.dep_centersX, self.dep_centersY