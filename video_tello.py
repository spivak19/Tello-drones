import numpy as np
import cv2
import tello
import threading
from PIL import Image

tello = tello.tello_video(8889,'192.168.10.2')
while True:
    frame = tello.read()

    if frame is None or frame.size == 0:
        continue
    else:
        image = Image.fromarray(frame)
        cv2.imshow('tello', image)

    if cv2.waitKey(1) == 27:
        break
tello.__del__()



