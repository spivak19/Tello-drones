import cv2
import tello
import keyboard

print('Welcome to tello operating system!\n')
print('Keybindings: \n')
print('t- take off\t l- land')
print('u- up\t     j- down')
print('w- forward\t s- backward')
print('a- left\t     d- right')
print('e- counter clock wise\tq- clockwise')
print('Enjoy!')
tello = tello.tello(local_port=8889, local_ip='')

