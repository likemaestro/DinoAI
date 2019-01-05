import numpy as np
from grabscreen import grab_screen
from random import shuffle
import cv2
import time
import win32api as wapi
import os

height = 16
width = 45

up =    [1,0,0]
down =  [0,1,0]
nk =    [0,0,1]

starting_value = 1
final_dir = os.path.join(os.getcwd(), r'data')
if not os.path.exists(final_dir):
           os.makedirs(final_dir)         
os.chdir(final_dir)

while True:
        file_name = 'training_data-{}.npy'.format(starting_value)
        
        if os.path.isfile(file_name):
            print('File exists, moving along',starting_value)
            starting_value += 1
        else:
            print('File does not exist, starting fresh!',starting_value)
            break

def keys_to_output():
    output = [0,0,0]
    if wapi.GetAsyncKeyState(0x26):
        output = up
    elif wapi.GetAsyncKeyState(0x28):
        output = down
    else:
        output = nk
    return output

def main(file_name, starting_value):
    file_name = file_name
    starting_value = starting_value
    training_data = []
    
    for i in list(range(1))[::-1]:
        print(i+1)
        time.sleep(1)

    last_time = time.time()
    paused = False
    print('STARTING!!!')
    while(True):
        if not paused:
            screen = grab_screen(region=(65,320,450+65,160+320))
            
            # resize to something a bit more acceptable for a CNN
            screen = cv2.resize(screen, (width,height))

            # run a color convert
            screen = cv2.cvtColor(screen, cv2.COLOR_BGR2GRAY)
            
            #set threshold for clean image
            ret, screen = cv2.threshold(screen,127,255,cv2.THRESH_BINARY_INV)
        
            output = keys_to_output()
            training_data.append([screen,output])
            
            cv2.imshow('window',cv2.resize(screen,(width,height)))
            if cv2.waitKey(25) & 0xFF == ord('q'):
                cv2.destroyAllWindows()
                break

            if len(training_data) % 100 == 0:
                print(len(training_data))
                
                if len(training_data) == 1000:
                    np.save(file_name,training_data)
                    print('SAVED')
                    training_data = []
                    starting_value += 1
                    file_name = 'training_data-{}.npy'.format(starting_value)

                    
        if wapi.GetAsyncKeyState(0x54):
            if paused:
                paused = False
                print('unpaused!')
                time.sleep(1)
            else:
                print('Pausing!')
                paused = True
                time.sleep(1)



##    training_data = []
##    for i in range(1,2):
##        training_data = np.load('training_data-{}.npy'.format(i))

##    random.shuffle(training_data)
##
##    X = []
##    y = []
##    for game,label in training_data:
##        X.append(game)
##        y.append(label)
##        
##    X = np.array(X).reshape(-1, height, width, 1)
##    print(X.shape)
##    ##new_array = cv2.resize(X[0], (width, height))
##    ##plt.imshow(new_array, cmap='gray')
##    ##plt.show()
##
##    pickle_out = open("X.pickle","wb")
##    pickle.dump(X, pickle_out)
##    pickle_out.close()
##
##    pickle_out = open("y.pickle","wb")
##    pickle.dump(y, pickle_out)
##    pickle_out.close()

main(file_name, starting_value)
