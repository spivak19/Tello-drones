import keyboard
import time



while True:  # making a loop
    try:  # used try so that if user pressed other than the given key error will not be shown
        if keyboard.is_pressed('w'):  # if key 'q' is pressed 
            print('You Pressed W!')
            time.sleep(0.2)  # finishing the loop
        if keyboard.is_pressed('s'):  # if key 's' is pressed 
            print('You Pressed S!')
            time.sleep(0.2)  # finishing the loop
        if keyboard.is_pressed('D'):  # if key 'd' is pressed 
            print('You Pressed D!')
            time.sleep(0.2)  # finishing the loop
        if keyboard.is_pressed('A'):  # if key 'a' is pressed 
            print('You Pressed A!')
            time.sleep(0.2)  # finishing the loop
    except:
        break  # if user pressed a key other than the given key the loop will break 
