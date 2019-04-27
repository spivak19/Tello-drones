import cv2
import numpy as np
import requests
import imutils
import argparse

ap = argparse.ArgumentParser()
ap.add_argument("-v", "--video", help="path to the video file")
ap.add_argument("-a", "--min-area", type=int, default=500, help="minimum area size")
args = vars(ap.parse_args())
url ='http://192.168.1.22:8000/stream.jpg'

cap = cv2.VideoCapture()
cap.open(url)
scale_percent = 50
first_frame = None
while True:
    ret , img_temp = cap.read()
    width = int(1920 * scale_percent / 100)
    height = int(1080 * scale_percent / 100)
    dim = (width, height)
    img = cv2.resize(img_temp, dim)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (21, 21), 0)

    if first_frame is None:
        first_frame = gray
        continue

    frameDelta = cv2.absdiff(first_frame, gray)
    thresh = cv2.threshold(frameDelta, 20, 255, cv2.THRESH_BINARY)[1]
    #thresh = cv2.dilate(thresh, None, iterations=2)
    thresh = cv2.dilate(thresh, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (11, 11)), iterations=4)
    thresh = cv2.dilate(thresh, None, iterations=2)


    cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,
                            cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)
    for c in cnts:
        if cv2.contourArea(c) < args["min_area"]:
            continue
        (x, y, w, h) = cv2.boundingRect(c)
        cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)

    cv2.imshow('threshold', thresh)
    cv2.imshow('original', img)
    cv2.imshow('', frameDelta)
    if cv2.waitKey(1) == 27:
        break
cv2.destroyAllWindows()



