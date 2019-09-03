import cv2
import numpy as np
import requests
import math
from return_image import return_frame
from hole_fill import hole_fill
import threading
import time
import Queue
import PIL

def write_to_xl():
    text_file_out = open("Output.txt", "w")
    text_file_out.write("Purchase Amount:\nhello")
    text_file_out.close()

    text_file_location = open("Output.txt", "w")
    text_file_location.write("Purchase Amount:\nhello")
    text_file_location.close()

def color_recognition():

    video1 = cv2.VideoCapture(0)
    video2 = cv2.VideoCapture(1)
    _, frame1 = video1.read()
    _, frame2 = video2.read()
    h, w, _ = frame1.shape
    print(h, w)
    x1 = w/2
    y1 = h/2

    x2 = w/2
    y2 = h/2

    roi1 = cv2.imread("frame2_tubleron.jpg", 1)
    roi2 = cv2.imread("frame2_tubleron.jpg", 1)

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
    counter3 = 1
    num = 10
    text_file_out = open("Output.txt", "w")
    text_file_out.close()
    text_file_out = open("location.txt", "a")

    text_file_location = open("location.txt", "w")
    text_file_location.close()
    text_file_location = open("location.txt", "a")

    x_axis = 0
    y_axis = 0
    z_axis = 0


    while True:
        _, frame1 = video1.read()
        _, frame2 = video2.read()

        hsv1 = cv2.cvtColor(frame1, cv2.COLOR_BGR2HSV)
        mask1 = cv2.calcBackProject([hsv1], [0], roi_hist1, [0, 180], 1)
        # mask = cv2.dilate(mask, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3)), iterations=3)
        # mask = cv2.erode(mask, cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3)), iterations=1)
        # smask = cv2.dilate(mask, cv2.getStructuringElement(cv2.MORPH_RECT, (20, 20)), iterations=2)

        satNmask1 = cv2.bitwise_and(hsv1[:, :, 1], mask1)
        satNmask1 = cv2.dilate(satNmask1, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3)), iterations=3)
        satNmask1 = cv2.erode(satNmask1, cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3)), iterations=1)
        threshold_indices1 = satNmask1 < 40
        satNmask1[threshold_indices1] = 0
        # satNmask = cv2.dilate(satNmask, cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5)), iterations=2)


        hsv2 = cv2.cvtColor(frame2, cv2.COLOR_BGR2HSV)
        mask2 = cv2.calcBackProject([hsv2], [0], roi_hist2, [0, 180], 1)
        # mask = cv2.dilate(mask, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3)), iterations=3)
        # mask = cv2.erode(mask, cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3)), iterations=1)
        # smask = cv2.dilate(mask, cv2.getStructuringElement(cv2.MORPH_RECT, (20, 20)), iterations=2)

        satNmask2 = cv2.bitwise_and(hsv2[:, :, 1], mask2)
        satNmask2 = cv2.dilate(satNmask2, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3)), iterations=3)
        satNmask2 = cv2.erode(satNmask2, cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3)), iterations=1)
        threshold_indices2 = satNmask2 < 85
        satNmask2[threshold_indices2] = 0
        # satNmask = cv2.dilate(satNmask, cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5)), iterations=2)

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

        ret1, track_window1 = cv2.CamShift(median_1, (x1, y1, width1, height1), term_criteria)
        x1, y1, w1, h1 = track_window1
        pts1 = cv2.boxPoints(ret1)  # add cv. after cv2
        pts1 = np.intp(pts1)
        cv2.polylines(frame1,[pts1],True, 255,2)
        cv2.circle(frame1, (x1 + int(round(0.5 * w1)), y1 + int(round(0.5 * h1))), 5, (0, 0, 255), -1)
        font = cv2.FONT_HERSHEY_SIMPLEX

        ret2, track_window2 = cv2.CamShift(median_2, (x2, y2, width2, height2), term_criteria)
        x2, y2, w2, h2 = track_window2
        pts2 = cv2.boxPoints(ret2)  # add cv. after cv2.
        pts2 = np.intp(pts2)
        cv2.polylines(frame2, [pts2], True, 255, 2)
        cv2.circle(frame2, (x2 + int(round(0.5 * w2)), y2 + int(round(0.5 * h2))), 5, (0, 0, 255), -1)

        distance = abs(x1 - x2)
        new_dist = 0
        if distance != 0:
            new_dist = 5000/distance
        else:
            new_dist = new_dist
        cv2.putText(frame1, str(distance), ((x1 + int(round(0.5 * w1))), y1 + 4 + int(round(0.5 * h1))), font, 1,
                    (0, 0, 255), 2)
        cv2.putText(frame2, str(distance), ((x2 + int(round(0.5 * w2))), y2 + 4 + int(round(0.5 * h2))), font, 1,
                    (0, 0, 255), 2)
        phi = (min(x1,x2) + 0.5*abs(x1-x2) - 320) * 0.109375
        theta = (min(y1,y2) + 0.5*abs(y1-y2) ) * 0.113 + 62.86

        x_axis_temp = new_dist * math.sin(math.radians(theta)) * math.cos(math.radians(phi))
        y_axis_temp = new_dist * math.sin(math.radians(theta)) * math.sin(math.radians(phi))
        z_axis_temp = new_dist * math.cos(math.radians(theta))
        if (x_axis+ y_axis+ z_axis == 0) or (abs(x_axis - x_axis_temp) <50 and abs(y_axis - y_axis_temp) <50 and abs(z_axis - z_axis_temp) <50):
            x_axis = x_axis_temp
            y_axis = y_axis_temp
            z_axis = z_axis_temp


        cv2.imshow('frame1', frame1)
        cv2.imshow('frame2', frame2)
        cv2.imshow('median_1', median_1)
        cv2.imshow('median_2', median_2)
        if counter3 == 1:
            #text_file_out.write("theta =%d, phi =%d, distance = %f   x =%f,y =%f,z =%f   \n" % (theta,phi, new_dist, x_axis, y_axis, z_axis))
            text_file_location.write("%f\t%f\t%f\n" % (x_axis, y_axis, z_axis))

            counter3 = 1
        else:
            counter3 += 1
        # cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
        #cv2.imshow("Mask1", mask1)
        #cv2.imshow("sat1",hsv1[:,:,1])

        #cv2.imshow("satNmask1", satNmask1)
        # cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
        # cv2.imshow("Mask2", mask2)
        # cv2.imshow("sat2",hsv2[:,:,1])
        #cv2.imshow("satNmask2", satNmask2)
        # cv2.imshow("average satNmask2",satNmask2_temp)

        key = cv2.waitKey(1)
        if key == 27:
            break
    video1.release()
    video2.release()

    cv2.destroyAllWindows()


def take_pictue():
    video1 = cv2.VideoCapture(0)
    video2 = cv2.VideoCapture(1)
    _, frame1 = video1.read()
    _, frame2 = video2.read()
    while True:
        r1, frame1 = video1.read()
        r2, frame2 = video2.read()
        if r1 and r2:
            cv2.imshow('frame1', frame1)
            cv2.imshow('frame2', frame2)

        if cv2.waitKey(1) == 27:
            break
    cv2.imwrite('frame1.jpg', frame1)
    cv2.imwrite('frame2.jpg', frame2)

def motion_detection():
    video1 = cv2.VideoCapture(0)
    video2 = cv2.VideoCapture(1)
    text_file_location = open("location.txt", "w")
    text_file_location.close()
    text_file_location = open("location.txt", "a")

    x_axis = 0
    y_axis = 0
    z_axis = 0

    cx_1 = 0
    cy_1 = 0
    cx_2 = 0
    cy_2 = 0
    for i in range(1, 100):
        back_1 = video1.read()
        back_2 = video2.read()
    while True:
        ret1, back_1 = video1.read()
        ret2, back_2 = video2.read()
        back_1_blurred = cv2.cvtColor(back_1, cv2.COLOR_BGR2GRAY)
        back_2_blurred = cv2.cvtColor(back_2, cv2.COLOR_BGR2GRAY)
        back_1_blurred = cv2.GaussianBlur(back_1_blurred, (21, 21), 0)
        back_2_blurred = cv2.GaussianBlur(back_2_blurred, (21, 21), 0)
        ret1_1, frame1 = video1.read()
        ret1_2, frame2 = video2.read()



        if ret1_1 and ret1_2:
            gray1 = cv2.cvtColor(frame1, cv2.COLOR_BGR2GRAY)
            gray2 = cv2.cvtColor(frame2, cv2.COLOR_BGR2GRAY)
            blurred1 = cv2.GaussianBlur(gray1, (21, 21), 0)
            blurred2 = cv2.GaussianBlur(gray2, (21, 21), 0)
            diff_frame_1 = cv2.absdiff(blurred1, back_1_blurred)
            thresh_frame_1 = cv2.threshold(diff_frame_1, 10, 255, cv2.THRESH_BINARY)[1]
            thresh_frame_1 = cv2.dilate(thresh_frame_1, None, iterations=4)
            cnts_1, _ = cv2.findContours(thresh_frame_1, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
            try:
                cnt_1 = cnts_1[0]
                M_1= cv2.moments(cnt_1)
                cx_1 = int(M_1['m10'] / M_1['m00'])
                cy_1 = int(M_1['m01'] / M_1['m00'])
                #if float(w1/h1)<0.9 and float(w1/h1)>0.3:
                x1, y1, w1, h1 = cv2.boundingRect(cnt_1)
                cv2.rectangle(frame1, (x1, y1), (x1 + w1, y1 + h1), (0, 255, 0), 2)
                #else:
                 #   continue
            except:
                cx_1 = cx_1
                cy_1 = cy_1
            #for contour_1 in cnts_1:
#
#               (x1, y1, w1, h1) = cv2.boundingRect(contour_1)
#              if w1/h1 < 1:
                 #   continue

                # making green rectangle arround the moving object
#                cv2.rectangle(frame1, (x1, y1), (x1 + w1, y1 + h1), (0, 255, 0), 3)
            diff_frame_2 = cv2.absdiff(blurred2, back_2_blurred)
            thresh_frame_2 = cv2.threshold(diff_frame_2, 10, 255, cv2.THRESH_BINARY)[1]
            thresh_frame_2 = cv2.dilate(thresh_frame_2, None, iterations=4)
            cnts_2, _ = cv2.findContours(thresh_frame_2, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
            try:
                cnt_2 = cnts_2[0]
                M_2= cv2.moments(cnt_2)
                cx_2 = int(M_2['m10'] / M_2['m00'])
                cy_2 = int(M_2['m01'] / M_2['m00'])
            #    if float(w2/h2)<0.9 and float(w2/h2)>0.3:
                x2, y2, w2, h2 = cv2.boundingRect(cnt_1)
                cv2.rectangle(frame2, (x2, y2), (x2 + w2, y2 + h2), (0, 255, 0), 2)
            #    else:
            #        continue
            except:
                cx_2 = cx_2
                cy_2 = cy_2
            #for contour_2 in cnts_2:

            #    (x2, y2, w2, h2) = cv2.boundingRect(contour_2)
                #if w2 / h2 < 1:
                #    continue
                # making green rectangle arround the moving object
            #    cv2.rectangle(frame2, (x2, y2), (x2 + w2, y2 + h2), (0, 255, 0), 3)

            distance = abs(cx_1 - cx_2)
            new_dist = 0
            if distance != 0:
                new_dist = 5000 / distance
            else:
                new_dist = new_dist

            phi = (min(cx_1, cx_2) + 0.5 * abs(cx_1 - cx_2) - 320) * 0.109375
            theta = (min(cy_1, cy_2) + 0.5 * abs(cy_1 - cy_2)) * 0.113 + 62.86

            x_axis_temp = new_dist * math.sin(math.radians(theta)) * math.cos(math.radians(phi))
            y_axis_temp = new_dist * math.sin(math.radians(theta)) * math.sin(math.radians(phi))
            z_axis_temp = new_dist * math.cos(math.radians(theta))
            if (x_axis + y_axis + z_axis == 0) or (x_axis_temp+y_axis_temp+z_axis_temp !=0):
                    #abs(x_axis - x_axis_temp) < 50 and abs(y_axis - y_axis_temp) < 50 and abs(
                #    z_axis - z_axis_temp) < 50):
                x_axis = x_axis_temp
                y_axis = y_axis_temp
                z_axis = z_axis_temp
            if x_axis+y_axis+z_axis !=0:
                text_file_location.write("%f\t%f\t%f\n" % (x_axis, y_axis, z_axis))


            cv2.imshow('frame1', frame1)
            cv2.imshow('frame2', frame2)
            cv2.imshow('dif1', thresh_frame_1)
            cv2.imshow('dif2', thresh_frame_2)

            if cv2.waitKey(1) == 27:
                break
if __name__ == '__main__':
    motion_detection()