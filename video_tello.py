import cv2
from PIL import Image
import numpy as np


def video_stream(tello):
    tello = tello.tello_video(local_port=8889,local_ip='')
    while True:
        frame = tello.read()
        if frame is None or frame.size == 0:
            continue
        else:
            image = Image.fromarray(frame)
            opencvImage = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
            cv2.imshow('video', opencvImage)

        if cv2.waitKey(1) == 27:
            break
    tello.__del__()



