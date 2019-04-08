import time
import tello


def main():
    drone = tello.tello(local_port=8889, local_ip='')
    time.sleep(5)
    tello.send_command2('takeoff')
    print('takeoff')
    time.sleep(5)
    tello.send_command2('land')


if __name__ == "__main__":
    main()
'''
video_thread = threading
tello.tello_video(tello)

time.sleep(5)
tello.takeoff()
print('takeoff')
time.sleep(10)
tello.land()
print('land')
'''