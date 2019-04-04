import cv2
import numpy as np
import functions


cap=cv2.VideoCapture(0);
while(True):

    ret, frame = cap.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    function = functions.Functions(gray)

    gauss = function.gauss    #Gaussian blur

    img_sobel = function.sobel(3,3)
    img_canny = cv2.Canny(gauss, 100, 20,9)                     #canny edge detection
    img_prewitt= function.prewitt()
    auto_canny = function.auto_canny(0.5)
    
    #cv2.imshow('sobel',img_sobel)
    cv2.imshow('auto canny', auto_canny)
    #cv2.imshow('prewitt', img_prewitt)
    #cv2.imshow('frame', gray)

    if cv2.waitKey(1) == 27:
        break

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()

