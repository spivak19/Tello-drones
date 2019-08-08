import cv2
import numpy as np
import requests
import math
from return_image import return_frame
from hole_fill import hole_fill
import Queue
import threading
import time

class recognition_class:
    def __init__(self):

        #Recognition og the drone via algorithms
        self.mask_color_right = None
        self.mask_color_left = None

        self.cap1 = cv2.VideoCapture(2)
        self.cap2 = cv2.VideoCapture(1)


        #X Coordinate
        self.right_x = None
        self.left_x = None

        #Left and Right frames
        self.left_image = None
        self.right_image = None

        #The images from both cameras
        #self.receive_image_thread = threading.Thread(target=self._receive_image_thread)
        #self.receive_image_thread.daemon = False
        #self.receive_image_thread.start()

        self.color_recognition = threading.Thread(target=self._color_recognition)
        self.color_recognition.daemon = False
        self.color_recognition.start()



    def _receive_image_thread(self):
        while True:
            _, self.left_image = self.cap1.read()
            _, self.right_image = self.cap2.read()
            if cv2.waitKey(1) == 27:
                break
        cv2.destroyAllWindows()

    def _color_recognition(self):
        while not(self.cap1.isOpened()) and not(self.cap2.isOpened()):
            continue

        while True:
            _, self.left_image = self.cap1.read()
            _, self.right_image = self.cap2.read()
            hsv_left = cv2.cvtColor(self.left_image, cv2.COLOR_BGR2HSV)
            hsv_right = cv2.cvtColor(self.right_image, cv2.COLOR_BGR2HSV)

            # define range of blue color in HSV
            lower_yellow1 = np.array([31, 100, 100])
            upper_yellow = np.array([41, 255, 255])

            # Threshold the HSV image to get only yellow color
            mask_right = cv2.inRange(hsv_right, lower_yellow1, upper_yellow)
            mask_left = cv2.inRange(hsv_left, lower_yellow1, upper_yellow)

            # mask = cv2.erode(mask, cv2.getStructuringElement(cv2.MORPH_RECT, (2, 4)), iterations=1)
            mask_right = cv2.dilate(mask_right, cv2.getStructuringElement(cv2.MORPH_RECT, (40, 40)), iterations=1)
            mask_left = cv2.dilate(mask_left, cv2.getStructuringElement(cv2.MORPH_RECT, (40, 40)), iterations=1)

            self.mask_color_right = hole_fill(mask_right)
            self.mask_color_left = hole_fill(mask_left)
            contours_right, _ = cv2.findContours(self.mask_color_right, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
            for c in contours_right:
                rect = cv2.boundingRect(c)
                if rect[2] < 100 or rect[3] < 100: continue
                self.right_x, y, w, h = cv2.boundingRect(c)
            try:
                cv2.rectangle(self.right_image, (self.right_x, y), (self.right_x + w, y + h), (0, 255, 0), 2)
                cv2.imshow("Show", self.right_image)

            except:
                cv2.imshow("Show", self.right_image)
            if cv2.waitKey(1) == 27:
                break
        cv2.destroyAllWindows()
