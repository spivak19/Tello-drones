import cv2
import numpy as np
import requests
import imutils
import argparse

time_for_reset = 20
counter_limit = time_for_reset*24

ap = argparse.ArgumentParser()
ap.add_argument("-v", "--video", help="path to the video file")
ap.add_argument("-a", "--min-area", type=int, default=1000, help="minimum area size")
args = vars(ap.parse_args())

#In the url - DONT FORGET THE PORT!!!
#url ='http://192.168.1.47:8000/stream.jpg'
url ='http://192.168.1.22:8000/stream.jpg'

cap = cv2.VideoCapture()
cap.open(url)

first_frame = None
second_frame = None
counter=0
scale_percent = 50
while True:
    ret, img_temp = cap.read()
    width = int(1920 * scale_percent / 100)
    height = int(1080 * scale_percent / 100)
    dim = (width, height)
    img = cv2.resize(img_temp, dim)

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (21, 21), 0)
    if first_frame is None and second_frame is None:
        first_frame = gray
        second_frame = gray
        continue
    counter += 1
    if counter == counter_limit:
        counter = 0
        first_frame = gray


    frameDelta = cv2.absdiff(first_frame, second_frame)
    thresh = cv2.threshold(frameDelta, 30, 255, cv2.THRESH_BINARY)[1]
    #thresh = cv2.dilate(thresh, None, iterations=2)
    thresh = cv2.dilate(thresh, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (11, 11)), iterations=5)
    thresh = cv2.dilate(thresh, None, iterations=2)
    cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,
                            cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)
    for c in cnts:
        if cv2.contourArea(c) < args["min_area"]:
            continue
        (x, y, w, h) = cv2.boundingRect(c)
        cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)
    M = cv2.moments(thresh)
    '''
    try:
        cX = int(M["m10"] / M["m00"])
        cY = int(M["m01"] / M["m00"])
        cv2.circle(img, (cX, cY), 5, (0, 255, 0), -1)
        cv2.imshow('original', img)
    except:
        cv2.imshow('original', img)
'''
    cv2.imshow('original', img)
    cv2.imshow('threshold', thresh)
    cv2.imshow('', frameDelta)
    second_frame = gray
    if cv2.waitKey(1) == 27:
        break
cv2.destroyAllWindows()