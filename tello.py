import cv2
import numpy as np
import argparse
import socket
import threading
import time
import libh264decoder
from PIL import Image


class tello:

    def __init__(self,local_port , local_ip,
                 tello_ip='192.168.10.1' ,tello_port=8889):

        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # socket for sending cmd
        self.decoder = libh264decoder.H264Decoder()
        self.frame = None
        self.last_frame = None
        self.socket_video = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.tello_address = (tello_ip, tello_port)
        self.local_video_port = 11111
        self.socket.bind((local_ip, local_port))
        #command = map(bin,bytearray('command'))
        #' '.join(map(bin,bytearray(command)))

        #streamon = map(bin, bytearray('streamon'))
        #' '.join(map(bin, bytearray(streamon)))

        #self.socket.sendto(command, self.tello_address)
        #print ('sent: command')
        #self.socket.sendto(streamon, self.tello_address)
        #print ('sent: streamon')
        self.socket_video.bind((local_ip, self.local_video_port))

        self.receive_video_thread = threading.Thread(target=self._receive_video_thread)
        self.receive_video_thread.daemon = True

        self.receive_video_thread.start()

    def __del__(self):
        """Closes the local socket."""
        self.socket.close()
        self.socket_video.close()

    def read(self):
        """Return the last frame from camera."""
        return self.frame

    def _receive_video_thread(self):
        """
        Listens for video streaming (raw h264) from the Tello.

        Runs as a thread, sets self.frame to the most recent frame Tello captured.

        """
        packet_data = ""
        while True:
            try:
                res_string, ip = self.socket_video.recvfrom(2048)
                packet_data += res_string
                # end of frame
                if len(res_string) != 1460:
                    for frame in self._h264_decode(packet_data):
                        self.frame = frame
                    packet_data = ""

            except socket.error as exc:
                print ("Caught exception socket.error : %s" % exc)

    def _h264_decode(self, packet_data):
        """
        decode raw h264 format data from Tello

        :param packet_data: raw h264 data array

        :return: a list of decoded frame
        """
        res_frame_list = []
        frames = self.decoder.decode(packet_data)
        for framedata in frames:
            (frame, w, h, ls) = framedata
            if frame is not None:
                # print 'frame size %i bytes, w %i, h %i, linesize %i' % (len(frame), w, h, ls)

                frame = np.fromstring(frame, dtype=np.ubyte, count=len(frame), sep='')
                frame = (frame.reshape((h, ls / 3, 3)))
                frame = frame[:, :w, :]
                res_frame_list.append(frame)

        return res_frame_list

    def video_stream(tello):
        # tello = tello.tello(local_port=8889,local_ip='')
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