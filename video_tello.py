import cv2
from PIL import Image
import numpy as np
import tello
import functions


functions = functions.Functions(None)
tello = tello.tello(local_port=8889,local_ip='')
while True:
    frame = tello.read()
    if frame is None or frame.size == 0:
        continue
    else:
        image = Image.fromarray(frame)
        img = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
        functions.image = img
        cv2.imshow('video', img)

    if cv2.waitKey(1) == 27:
        break
tello.__del__()



