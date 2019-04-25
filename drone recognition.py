import cv2
import numpy as np
import requests

url ='http://10.100.102.36:8080/shot.jpg'
yellow= np.uint8([[[14,234,219 ]]])
hsv_yellow = cv2.cvtColor(yellow,cv2.COLOR_BGR2HSV)
print hsv_yellow

scale_percent = 70

while(True):
    img_resp = requests.get(url)
    img_arr = np.array(bytearray(img_resp.content), dtype=np.uint8)
    img_temp= cv2.imdecode(img_arr, -1)

    width = int(960 * scale_percent / 100)
    height = int(540 * scale_percent / 100)
    dim = (width, height)

    img = cv2.resize(img_temp, dim)#interpolation=cv2.INTER_AREA)

    '''
    _, frame = cap.read()
    '''
    # Convert BGR to HSV
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    # define range of blue color in HSV
    lower_blue = np.array([22,100,100])
    upper_blue = np.array([43,255,255])

    # Threshold the HSV image to get only yellow color
    mask_temp = cv2.inRange(hsv, lower_blue, upper_blue)

    mask_dilated = cv2.dilate(mask_temp, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3)), iterations=3)

    mask_eroded = cv2.erode(mask_dilated, cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3)), iterations=5)

    mask = cv2.dilate(mask_eroded, cv2.getStructuringElement(cv2.MORPH_RECT, (20, 20)), iterations=2)
    M = cv2.moments(mask)
    res = cv2.bitwise_and(img,img, mask= mask)
    try:
        cX = int(M["m10"] / M["m00"])
        cY = int(M["m01"] / M["m00"])
        cv2.circle(res, (cX, cY), 5, (0, 255, 0), -1)
        cv2.imshow('res', res)
    except:
        cv2.imshow('res', res)
    # Bitwise-AND mask and original image

    cv2.imshow('frame',img)
    cv2.imshow('mask',mask)


    if cv2.waitKey(1) == 27:
        break

cv2.destroyAllWindows()
