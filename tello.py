import cv2
import numpy as np
import argparse
import socket
import threading
import time
import libh264decoder
from PIL import Image
import keyboard

class tello:

    def __init__(self,local_port , local_ip,
                 tello_ip='192.168.10.1' ,tello_port=8889):

        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # socket for sending cmd
        self.decoder = libh264decoder.H264Decoder()
        self.frame = None
        self.last_frame = None
        self.image = None
        self.socket_video = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.tello_address = (tello_ip, tello_port)
        self.local_video_port = 11111
        self.socket.bind((local_ip, local_port))

        self.socket_video.bind((local_ip, self.local_video_port))

        self.receive_video_thread = threading.Thread(target=self._receive_video_thread)
        self.receive_video_thread.daemon = True
        self.receive_video_thread.start()

        self._send_command = threading.Thread(target=self.send_command)
        self._send_command.daemon = True
        self._send_command.start()

        self.video_show_thread = threading.Thread(target=self.video_stream)
        self.video_show_thread.daemon = False
        self.video_show_thread.start()

        self._manual_flight = threading.Thread(target=self.manual_flight)
        self._manual_flight.daemon = True
        self._manual_flight.start()

        self.socket.sendto(b'command', self.tello_address); print('sent: command')
        self.socket.sendto(b'streamon', self.tello_address); print('sent: streamon')

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


    def send_command(self):
        while True:
            self.socket.sendto(b'command', self.tello_address)
            time.sleep(1)
            self.socket.sendto(b'streamon', self.tello_address)
            time.sleep(5)

    def video_stream(self):
        # tello = tello.tello(local_port=8889,local_ip='')
        while True:
            frame = self.frame
            if frame is None or frame.size == 0:
                continue
            else:
                image = Image.fromarray(frame)
                opencvImage = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
                cv2.imshow('video', opencvImage)

            if cv2.waitKey(1) == 27:
                break
        tello.__del__()

    def takeoff(self):
        self.socket.sendto(b'takeoff', self.tello_address)

    def land(self):
        self.socket.sendto(b'land', self.tello_address)

    def forward(self):
        self.socket.sendto(b'forward 30', self.tello_address)

    def back(self):
        self.socket.sendto(b'back 30', self.tello_address)

    def right(self):
        self.socket.sendto(b'right 30', self.tello_address)

    def left(self):
        self.socket.sendto(b'left 30', self.tello_address)

    def up(self):
        self.socket.sendto(b'up 30', self.tello_address)

    def down(self):
        self.socket.sendto(b'down 30', self.tello_address)

    def cw(self):
        self.socket.sendto(b'cw 30', self.tello_address)

    def ccw(self):
        self.socket.sendto(b'ccw 30', self.tello_address)

    def battery(self):
        self.socket.sendto(b'battey?', self.tello_address)

    def flight_plan(self):
        time.sleep(1)
        self.takeoff();    print('takeoff')
        time.sleep(3)
        self.forward()
        time.sleep(3)
        self.back()
        time.sleep(3)
        self.cw()
        time.sleep(3)
        self.cw()
        time.sleep(3)
        self.land();       print('land')

    def manual_flight(self):
        while True:
            action = raw_input('please enter tello actions')
            if keyboard.is_pressed('t'):
                self.takeoff(); print('takeoff')
                continue
            if action == 'land':
                self.land(); print('land')
                continue
            if action == 'forward':
                self.forward(); print('forward')
                continue
            if action == 'back':
                self.back(); print('back')
                continue
            if action == 'right':
                self.right(); print('right')
                continue
            if action == 'left':
                self.left(); print('left')
                continue
            if action == 'up':
                self.up(); print('up')
                continue
            if action == 'down':
                self.down(); print('down')
                continue
            if action == 'cw':
                self.cw(); print('cw')
                continue
            if action == 'ccw':
                self.ccw(); print('ccw')
                continue
            else:
                print('Enter valid action')