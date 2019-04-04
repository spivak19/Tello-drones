import cv2
import numpy as np
import random
import argparse
import glob

class Functions:
    '''
     Add salt and pepper noise to image
      prob: Probability of the noise
     '''
    def __init__(self, image):
        self.image = image
        self.gauss = cv2.GaussianBlur(image,(1,1),0)

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

    def sobel(self,kx,ky):
        img_sobelx = cv2.Sobel(self.gauss, cv2.CV_8U, 1, 0, ksize=kx)  # sobel edge detection
        img_sobely = cv2.Sobel(self.gauss, cv2.CV_8U, 0, 1, ksize=ky)
        img_sobel = img_sobelx + img_sobely
        return img_sobel

    def prewitt(self):
        kernelx = np.array([[1, 1, 1], [0, 0, 0], [-1, -1, -1]])  # prewitt edge detection
        kernely = np.array([[-1, 0, 1], [-1, 0, 1], [-1, 0, 1]])
        img_prewittx = cv2.filter2D(self.gauss, -1, kernelx)
        img_prewitty = cv2.filter2D(self.gauss, -1, kernely)
        img_prewitt = img_prewittx + img_prewitty
        return img_prewitt

    def auto_canny(self, sigma=0.33):
        # compute the median of the single channel pixel intensities
        v = np.median(self.image)

        # apply automatic Canny edge detection using the computed median
        lower = int(max(0, (1.0 - sigma) * v))
        upper = int(min(255, (1.0 + sigma) * v))
        edged = cv2.Canny(self.image, lower, upper)

        # return the edged image
        return edged