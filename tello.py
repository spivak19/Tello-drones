import cv2
import numpy as np
import argparse
import socket
import threading
import time
import libh264decoder
from PIL import Image
import keyboard
import os

class tello:

    def __init__(self,local_port , local_ip,
                 tello_ip='192.168.10.1' ,tello_port=8889):

        self.video_bool = False
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

        self.receive_thread = threading.Thread(target=self._receive_thread)
        self.receive_thread.daemon = True
        self.receive_thread.start()

        self._send_command = threading.Thread(target=self.send_command)
        self._send_command.daemon = True
        self._send_command.start()

        self.video_show_thread = threading.Thread(target=self.video_stream)
        self.video_show_thread.daemon = False
        self.video_show_thread.start()

        self._manual_flight = threading.Thread(target=self.manual_flight)
        self._manual_flight.daemon = True
        self._manual_flight.start()

        self._save_video = threading.Thread(target=self.save_video)
        self._save_video.daemon = True
        self._save_video.start()

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
            time.sleep(7)

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
                self.image = opencvImage
            if cv2.waitKey(1) == 27:
                break
        self.__del__()

    def _receive_thread(self):

        while True:
            try:
                self.response, ip = self.socket.recvfrom(3000)
                # print(self.response)
            except socket.error as exc:
                print ("Caught exception socket.error : %s" % exc)
            if self.response is None:
                response = 'none_response'
            else:
                response = self.response.decode('utf-8')
                print ('Tello: '+response)
            self.response = None

    def save_video(self):
        print('yes it is recording')
        FILE_OUTPUT = 'output.avi'
        if os.path.isfile(FILE_OUTPUT):
            os.remove(FILE_OUTPUT)
        fourcc = cv2.VideoWriter_fourcc(*'DIVX')
        out = cv2.VideoWriter(FILE_OUTPUT, fourcc, 60.0, (960, 720))
        while self.video_bool == False:
            continue
        while self.video_bool == True:
            out.write(self.image)
            print('saving video')
            if cv2.waitKey(1) == 27:
                break
        out.release()

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
        self.socket.sendto(b'battery?', self.tello_address)


    def flight_plan(self):
        time.sleep(1)

    def joystick_flight(self):
        while True:
            try:
                a = 0
                b = 0
                c = 0
                d = 0
                if keyboard.is_pressed('6'):  # move right
                    a = a+50
                if keyboard.is_pressed('4'):  # move left
                    a = a-50

                if keyboard.is_pressed('8'):  # move forward
                    b = b+50
                if keyboard.is_pressed('5'):  # move backward
                    b = b-50

                if keyboard.is_pressed('u'):  # move up
                    c = c+50
                if keyboard.is_pressed('j'):  # move down
                    c = c-50

                if keyboard.is_pressed('9'):  # move cw
                    d = d+150
                if keyboard.is_pressed('7'):  # move ccw
                    d = d-150

                self.socket.sendto(b'rc ' + str(a) + ' '+str(b) + ' '
                                   + str(c) + ' ' + str(d), self.tello_address)
            except:
                break  # if user pressed a key other than the given key the loop will break
            

    def manual_flight(self):
        while True:  # making a loop
            try:  # used try so that if user pressed other than the given key error will not be shown
                if keyboard.is_pressed('w'):  # move forward
                    self.forward()
                    time.sleep(0.2)  
                if keyboard.is_pressed('s'):  # Move backward
                    self.back()
                    time.sleep(1)  
                if keyboard.is_pressed('d'):  # Move right
                    self.right()
                    time.sleep(1)  
                if keyboard.is_pressed('a'):  # Move left
                    self.left()
                    time.sleep(1)  
                if keyboard.is_pressed('b'):  # Display battery percentage
                    self.battery()
                    time.sleep(1)  
                if keyboard.is_pressed('t'):  # Take off
                    self.takeoff()
                    time.sleep(1)  
                if keyboard.is_pressed('l'):  # Land
                    self.land()
                    time.sleep(1)  
                if keyboard.is_pressed('i'):  # Move up
                    self.up()
                    time.sleep(1)  
                if keyboard.is_pressed('k'):  # Move down
                    self.down()
                    time.sleep(1)  
                if keyboard.is_pressed('e'):  # rotate clock wise
                    self.cw()
                    time.sleep(1)  
                if keyboard.is_pressed('q'):  # rotate counter clock wise
                    self.ccw()
                    time.sleep(1)

                a = 0
                b = 0
                c = 0
                d = 0
                if keyboard.is_pressed('6'):  # move right
                    a = a+50
                if keyboard.is_pressed('4'):  # move left
                    a = a-50

                if keyboard.is_pressed('8'):  # move forward
                    b = b+50
                if keyboard.is_pressed('5'):  # move backward
                    b = b-50

                if keyboard.is_pressed('u'):  # move up
                    c = c+50
                if keyboard.is_pressed('j'):  # move down
                    c = c-50

                if keyboard.is_pressed('9'):  # move cw
                    d = d+50
                if keyboard.is_pressed('7'):  # move ccw
                    d = d-50

                self.socket.sendto(b'rc ' + str(a) + ' '+str(b) + ' '
                                   + str(c) + ' ' + str(d), self.tello_address)
                if keyboard.is_pressed('v') and not self.video_bool:  # save video to file
                    print('saving video')
                    self.video_bool = True
                    time.sleep(1)
                if keyboard.is_pressed('v') and self.video_bool:  # save video to file
                    print('stopping video')
                    self.video_bool = False
                    time.sleep(1)
            except:
                break  # if user pressed a key other than the given key the loop will break
