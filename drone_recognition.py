import cv2
import numpy as np
import requests
import math
from return_image import return_frame
from hole_fill import hole_fill

def drone_recognition(frame, saturation_value=100, scale_percent=100):
    # Convert BGR to HSV
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # define range of blue color in HSV
    lower_yellow1 = np.array([31,saturation_value,100])
    upper_yellow = np.array([41,255,255])

    # Threshold the HSV image to get only yellow color
    mask_temp = cv2.inRange(hsv, lower_yellow1, upper_yellow)
    mask = mask_temp
    #mask = cv2.erode(mask, cv2.getStructuringElement(cv2.MORPH_RECT, (2, 4)), iterations=1)
    mask = cv2.dilate(mask, cv2.getStructuringElement(cv2.MORPH_RECT, (40, 40)), iterations=1)
    mask = hole_fill(mask)

    #return mask_temp
    return mask


if __name__ == '__main__':
    cap1 = cv2.VideoCapture(1)
    cap2 = cv2.VideoCapture(0)

    while True:
        frame1 = return_frame(cap1)
        frame2 = return_frame(cap2)


        mask1 = drone_recognition(frame1,100)
        mask2 = drone_recognition(frame2,100)

        M1 = cv2.moments(mask1)
        M2 = cv2.moments(mask2)

        cx1f = 1
        cy1f = 1
        cx2f = 1
        cy2f = 1
        if M1["m00"] != 0:
            # calculate x,y coordinate of center
            cX1 = int(M1["m10"] / M1["m00"])
            cY1 = int(M1["m01"] / M1["m00"])
            cx1f = float(cX1)
            cy1f = float(cY1)
        else:
            cX1 = 1
            cY1 = 1
        if M2["m00"] != 0:
            cX2 = int(M2["m10"] / M2["m00"])
            cY2 = int(M2["m01"] / M2["m00"])
            cx2f = float(cX2)
            cy2f = float(cY2)
        else:
            cX2 = 1
            cY2 = 1

        multiplication1 = cv2.bitwise_and(frame1, frame1, mask=mask1)
        multiplication2 = cv2.bitwise_and(frame2, frame2, mask=mask2)

        d = ((math.pow((cx1f-cx2f),2) + math.pow((cy1f-cy2f), 2)))

        if d != 0:
            D = (4.56 / (d*7*math.pow(10,-6)))+47.14
        else:
            D = 0



        cv2.circle(multiplication1, (cX1, cY1), 5, (255, 255, 255), -1)
        cv2.putText(multiplication1, str(D), (cX1 - 25, cY1 - 25), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)

        cv2.circle(multiplication2, (cX2, cY2), 5, (255, 255, 255), -1)
        cv2.putText(multiplication2, "", (cX2 - 25, cY2 - 25), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)

        cv2.imshow('yellow drone_1', multiplication1)
        cv2.imshow('frame_1', frame1)
        cv2.imshow('mask1', mask1)

        cv2.imshow('yellow drone_2', multiplication2)
        cv2.imshow('frame_2', frame2)
        if cv2.waitKey(1) == 27:
            break
    cv2.destroyAllWindows()
