import cv2
import numpy as np
import Queue
video1 = cv2.VideoCapture(0)
video2 = cv2.VideoCapture(1)

x1=360
y1=0

x2=360
y2=0

roi1 = cv2.imread("image3.png",1)
roi2 = cv2.imread("image2.png",1)

width1 = 300
height1 = 120

width2 = 300
height2 = 120

hsv_roi1 = cv2.cvtColor(roi1, cv2.COLOR_BGR2HSV)
roi_hist1 = cv2.calcHist([hsv_roi1], [0], None, [180], [0, 180])
roi_hist1[0] = 0
roi_hist1 = cv2.normalize(roi_hist1, roi_hist1, 0, 255, cv2.NORM_MINMAX)

hsv_roi2 = cv2.cvtColor(roi2, cv2.COLOR_BGR2HSV)
roi_hist2 = cv2.calcHist([hsv_roi2], [0], None, [180], [0, 180])
roi_hist2[0] = 0
roi_hist2 = cv2.normalize(roi_hist2, roi_hist2, 0, 255, cv2.NORM_MINMAX)

term_criteria = (cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 10, 1)

medstack1 = []
medstack2 = []
counter1 = 1
counter2 = 1
num = 10
while True:
    _, frame1 = video1.read()
    _, frame2 = video2.read()

    hsv1 = cv2.cvtColor(frame1, cv2.COLOR_BGR2HSV)
    mask1 = cv2.calcBackProject([hsv1], [0], roi_hist1, [0, 180], 1)
    #mask = cv2.dilate(mask, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3)), iterations=3)
    #mask = cv2.erode(mask, cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3)), iterations=1)
    #smask = cv2.dilate(mask, cv2.getStructuringElement(cv2.MORPH_RECT, (20, 20)), iterations=2)
    
    satNmask1 = cv2.bitwise_and(hsv1[:,:,1],mask1)
    satNmask1 = cv2.dilate(satNmask1, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3)), iterations=3)
    satNmask1 = cv2.erode(satNmask1, cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3)), iterations=1)
    threshold_indices1 = satNmask1 < 40
    satNmask1[threshold_indices1] = 0
    #satNmask = cv2.dilate(satNmask, cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5)), iterations=2)

    ret1, track_window1 = cv2.CamShift(satNmask1, (x1, y1, width1, height1), term_criteria)
    x1, y1, w1, h1 = track_window1
    pts1 = cv2.cv.BoxPoints(ret1)
    pts1 = np.intp(pts1)
    #cv2.polylines(frame1,[pts1],True, 255,2)
    cv2.circle(frame1, (x1+ int(round(0.5*w1)) ,y1+ int(round(0.5*h1)) ), 5, (0,0,255), -1) 
    font = cv2.FONT_HERSHEY_SIMPLEX
    



    hsv2 = cv2.cvtColor(frame2, cv2.COLOR_BGR2HSV)
    mask2 = cv2.calcBackProject([hsv2], [0], roi_hist2, [0, 180], 1)
    #mask = cv2.dilate(mask, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3)), iterations=3)
    #mask = cv2.erode(mask, cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3)), iterations=1)
    #smask = cv2.dilate(mask, cv2.getStructuringElement(cv2.MORPH_RECT, (20, 20)), iterations=2)
    
    satNmask2 = cv2.bitwise_and(hsv2[:,:,1],mask2)
    satNmask2 = cv2.dilate(satNmask2, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3)), iterations=3)
    satNmask2 = cv2.erode(satNmask2, cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3)), iterations=1)
    threshold_indices2 = satNmask2 < 85
    satNmask2[threshold_indices2] = 0
    #satNmask = cv2.dilate(satNmask, cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5)), iterations=2)

    ret2, track_window2 = cv2.CamShift(satNmask2, (x2, y2, width2, height2), term_criteria)
    x2, y2, w2, h2 = track_window2
    pts2 = cv2.cv.BoxPoints(ret2)
    pts2 = np.intp(pts2)
    cv2.polylines(frame2,[pts2],True, 255,2)
    cv2.circle(frame2, (x2+ int(round(0.5*w2)) ,y2+ int(round(0.5*h2)) ), 5, (0,0,255), -1) 

    distance = abs(x1-x2)

    cv2.putText(frame1,str(distance),((x1+ int(round(0.5*w1))),y1+4+ int(round(0.5*h1))), font, 1,(0,0,255),2)
    cv2.putText(frame2,str(distance),((x2+ int(round(0.5*w2))),y2+4+ int(round(0.5*h2))), font, 1,(0,0,255),2)



    if counter1 < num:
        counter1 += 1
        medstack1.append(satNmask1)
        median_1 = np.median(medstack1, axis=0)
    else:
        _ = medstack1.pop(0)
        medstack1.append(satNmask1)
        median_1 = np.median(medstack1, axis=0)

    if counter2 < num:
        counter2 += 1
        medstack2.append(satNmask2)
        median_2 = np.median(medstack2, axis=0)
    else:
        _ = medstack2.pop(0)
        medstack2.append(satNmask2)
        median_2 = np.median(medstack2, axis=0)

    cv2.imshow('median_1',median_1)
    cv2.imshow('median_2',median_2)

    cv2.imshow('frame1',frame1)
    #cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
    #cv2.imshow("Mask1", mask1)
    #cv2.imshow("sat1",hsv1[:,:,1])
    
    cv2.imshow("satNmask1",satNmask1)


    cv2.imshow('frame2',frame2)
    #cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
    #cv2.imshow("Mask2", mask2)
    #cv2.imshow("sat2",hsv2[:,:,1])
    
    cv2.imshow("satNmask2",satNmask2)

    #cv2.imshow("average satNmask2",satNmask2_temp)
    
    key = cv2.waitKey(1)
    if key == 27:
        break
video1.release()
video2.release()


cv2.destroyAllWindows()