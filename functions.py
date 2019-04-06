import cv2
import numpy as np
import random
import argparse
import glob

class Functions:

    def __init__(self, image):
        self.image = image
        self.gauss = cv2.GaussianBlur(image,(1,1),0)

    # Colored and grayscale
    def salt_pepper(self , prob):
        out = np.zeros(self.image.shape, np.uint8)
        threshold = 1 - prob
        for i in range(self.image.shape[0]):
            for j in range(self.image.shape[1]):
               rand = random.random()
               if rand < prob:
                   out[i][j] = 0
               elif rand > threshold:
                   out[i][j] = 255
               else:
                   out[i][j] = self.image[i][j]
        return  out

    # Grayscale only!
    def sobel(self,kx,ky):
        img_sobelx = cv2.Sobel(self.gauss, cv2.CV_8U, 1, 0, ksize=kx)  # sobel edge detection
        img_sobely = cv2.Sobel(self.gauss, cv2.CV_8U, 0, 1, ksize=ky)
        img_sobel = img_sobelx + img_sobely
        return img_sobel

    # Grayscale only!
    def prewitt(self):
        kernelx = np.array([[1, 1, 1], [0, 0, 0], [-1, -1, -1]])  # prewitt edge detection
        kernely = np.array([[-1, 0, 1], [-1, 0, 1], [-1, 0, 1]])
        img_prewittx = cv2.filter2D(self.gauss, -1, kernelx)
        img_prewitty = cv2.filter2D(self.gauss, -1, kernely)
        img_prewitt = img_prewittx + img_prewitty
        return img_prewitt

    # Grayscale only!
    def auto_canny(self, sigma=0.33):
        # compute the median of the single channel pixel intensities
        v = np.median(self.image)

        # apply automatic Canny edge detection using the computed median
        lower = int(max(0, (1.0 - sigma) * v))
        upper = int(min(255, (1.0 + sigma) * v))
        edged = cv2.Canny(self.image, lower, upper)

        # return the edged image
        return edged

    # Colored only!
    #For video- Faster algorithm
    def face_video(self):
        img = self.image
        img= cv2.resize(img, (0,0), fx=0.5, fy=0.5)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
        face_detect = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5)
        face_detect
        for (x, y, w, h) in face_detect:
            cv2.rectangle(img, (x, y), (x + w, y + h), (0, 0, 255), 1)
        img= cv2.resize(img, (0,0), fx=2, fy=2)
        return img

    # Colored only!
    # For image
    def face_image(self):
        img = self.image
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_alt.xml')
        face_detect = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=1)
        face_detect
        for (x, y, w, h) in face_detect:
            cv2.rectangle(img, (x, y), (x + w, y + h), (0, 0, 255), 2)
        return img

    # Grayscale only!
    def dynamic_thresh(self):
        return cv2.adaptiveThreshold(self.image, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 115, 1)

    # Grayscale only!
    def hist_stretch(self, image):
        hist, bins = np.histogram(image.flatten(), 256, [0, 256])
        cdf = hist.cumsum()
        cdf_normalized = cdf * hist.max() / cdf.max()
        cdf_m = np.ma.masked_equal(cdf, 0)
        cdf_m = (cdf_m - cdf_m.min()) * 255 / (cdf_m.max() - cdf_m.min())
        cdf = np.ma.filled(cdf_m, 0).astype('uint8')
        return cdf[image]
