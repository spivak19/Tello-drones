import cv2
import functions

#hey sahar! i'm editing the code straightly from pycharm!
#please accept this commit!

img_temp = cv2.imread('lenna.jpg',0)
h, w = img_temp.shape
x_resize = 400
y_resize = x_resize*h/w
img=cv2.resize(img_temp, (x_resize, y_resize))

colored=functions.Functions(cv2.imread('lena.jpg'))

sp=functions.Functions(img)                   #salt and pepper noise
salt_and_pepper = sp.salt_pepper(0.1)

median = cv2.medianBlur(salt_and_pepper,3)      #median filter
hist_eq=cv2.equalizeHist(img)                   #equalize histogram

edge_detection = cv2.Canny(hist_eq,10,255)      #edge detection

hist_eq=cv2.equalizeHist(img)                   #equalize histogram
"""
histogram stretch
"""
stretched= sp.hist_stretch()


cv2.imshow('original image', img)
cv2.waitKey(0)
cv2.imshow('hist stretch' , stretched)
cv2.waitKey(0)
cv2.imshow('hist adjusted', hist_eq)
cv2.waitKey(0)
cv2.imshow('edge detection' , edge_detection)

cv2.waitKey(0)                                  #waits untill any keyboard event
cv2.destroyAllWindows()
