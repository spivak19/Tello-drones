import cv2
import numpy as np
video = cv2.VideoCapture(0)
x=360
y=0

roi = cv2.imread("image.png",1)
width = 300
height = 120
hsv_roi = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)
roi_hist = cv2.calcHist([hsv_roi], [0], None, [180], [0, 180])
roi_hist[0] = 0
roi_hist = cv2.normalize(roi_hist, roi_hist, 0, 255, cv2.NORM_MINMAX)
term_criteria = (cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 10, 1)
while True:
    _, frame = video.read()
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    mask = cv2.calcBackProject([hsv], [0], roi_hist, [0, 180], 1)
    #mask = cv2.dilate(mask, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3)), iterations=3)
    #mask = cv2.erode(mask, cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3)), iterations=1)
    #smask = cv2.dilate(mask, cv2.getStructuringElement(cv2.MORPH_RECT, (20, 20)), iterations=2)
    sat = hsv[:,:,1]
    sat = cv2.dilate(sat, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5)), iterations=2)
    satNmask = cv2.bitwise_and(sat,mask)
    satNmask = cv2.erode(satNmask, cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3)), iterations=1)
    satNmask = cv2.dilate(satNmask, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3)), iterations=2)
    satNmask = cv2.erode(satNmask, cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3)), iterations=1)
    threshold_indices = satNmask < 50
    satNmask[threshold_indices] = 0
    satNmask = cv2.equalizeHist(satNmask)
    #satNmask = cv2.dilate(satNmask, cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5)), iterations=2)

    ret, track_window = cv2.meanShift(satNmask, (x, y, width, height), term_criteria)
    x, y, w, h = track_window
    #pts = cv2.cv.BoxPoints(ret)
    #pts = np.intp(pts)
    #cv2.polylines(frame,[pts],True, 255,2)
    cv2.imshow('frame',frame)
    cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
    cv2.imshow("Mask", mask)
    cv2.imshow("sat1",hsv[:,:,1])
    cv2.imshow("satNmask",satNmask)
    
    key = cv2.waitKey(1)
    if key == 27:
        break
video.release()

cv2.destroyAllWindows()