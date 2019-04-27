import cv2
import numpy as np
import requests
import imutils
import argparse



ap = argparse.ArgumentParser()
ap.add_argument("-v", "--video", help="path to the video file")
ap.add_argument("-a", "--min-area", type=int, default=1000, help="minimum area size")
args = vars(ap.parse_args())

#url ='http://192.168.43.1:8080/shot.jpg'
#url ='http://192.168.1.37:8080/shot.jpg'
url ='http://192.168.43.1:8080/shot.jpg'

first_frame = None
second_frame = None
scale_percent = 70
while True:

    img_resp = requests.get(url)
    img_arr = np.array(bytearray(img_resp.content), dtype=np.uint8)
    img_temp = cv2.imdecode(img_arr, -1)

    width = int(960 * scale_percent / 100)
    height = int(540 * scale_percent / 100)
    dim = (width, height)
    img = cv2.resize(img_temp, dim)

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (21, 21), 0)

    if first_frame is None and second_frame is None:
        first_frame = gray
        continue

    second_frame = gray

    frameDelta = cv2.absdiff(first_frame, second_frame)
    thresh = cv2.threshold(frameDelta, 25, 255, cv2.THRESH_BINARY)[1]
    thresh = cv2.dilate(thresh, cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3)), iterations=3)

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
    first_frame = second_frame
    if cv2.waitKey(1) == 27:
        break
cv2.destroyAllWindows()