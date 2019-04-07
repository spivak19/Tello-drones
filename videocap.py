import cv2
import numpy as np
import functions

#initialize the video capture function
cap=cv2.VideoCapture(0)

while True:
    # get frames from web camera
    ret, frame = cap.read()

    # convert to grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)


    #Initiate the function class with grayscale image- the class that holds all of the functions
    function = functions.Functions(gray)
    colored = functions.Functions(frame)
    #initiate the function class with colored image
    #and start the face recognition function
    #face = colored.face_video()
    face = colored.face_video()
    # Gaussian blur
    #gauss = function.gauss

    # Sobel edge detection
    #img_sobel = function.sobel(3,3)

    # Canny edge detection- regular canny and auto canny
    #img_canny = cv2.Canny(gauss, 100, 20,9)
    #auto_canny = function.auto_canny(0.5)

    # prewitt edge detection
    #img_prewitt= function.prewitt()

    #Dynamic threshold
    #th = function.dynamic_thresh()

    #Print on screen
    cv2.imshow('face detection1', face)
    #cv2.imshow('sobel',img_sobel)
    #cv2.imshow('auto canny', auto_canny)
    #cv2.imshow('prewitt', img_prewitt)
    #cv2.imshow('canny', canny)
    #cv2.imshow('adaptive thresh', th)

    if cv2.waitKey(1) == 27:
        break

# When everything is done release the capture
cap.release()
cv2.destroyAllWindows()


