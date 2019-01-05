import numpy as np
from grabscreen import grab_screen
import cv2
import time
from tensorflow.keras.models import load_model
import numpy as np
import win32api as wapi
import pyautogui

height = 16
width = 45


model = load_model("Dino.model")

print('Start!!!!')

def main():
##    for i in list(range(4))[::-1]:
##        print(i+1)
##        time.sleep(1)

    paused = False
    mode_choice = 0

    while(True):
        
        if not paused:
            screen = grab_screen(region=(65,320,450+65,160+320))
            screen = cv2.cvtColor(screen, cv2.COLOR_BGR2GRAY)
            screen = cv2.resize(screen, (width,height))
            ret, screen = cv2.threshold(screen,127,255,cv2.THRESH_BINARY_INV)
            
            screen = screen.reshape(1,height, width, 1)
            
            prediction = model.predict(screen)[0]
            prediction = np.round(prediction)
            print(prediction)
            mode_choice = np.argmax(prediction)
            if mode_choice == 0:
                pyautogui.press('up')
            elif mode_choice == 1:
                pyautogui.press('down')
            else:
                pass
            
        if wapi.GetAsyncKeyState(0x54):
            if paused:
                paused = False
                print('unpaused!')
                time.sleep(1)
            else:
                print('Pausing!')
                paused = True
                time.sleep(1)

main()       
