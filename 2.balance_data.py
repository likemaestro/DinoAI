
from collections import Counter
import numpy as np
from random import shuffle
import pandas as pd
import cv2


for i in range(1,8+1):
    training_data = np.load('data/training_data-{}.npy'.format(i))
    #print(len(training_data))
    shuffle(training_data)

    ups = []
    downs = []
    nokeys = []

    shuffle(training_data)
    for data in training_data:
        img = data[0]
        key = data[1]
        if   key == [1,0,0]:
            ups.append([img,key])
        elif key == [0,1,0]:
            downs.append([img,key])
        elif key == [0,0,1]:
            nokeys.append([img,key])
        else:
            print('No Matches!!')


    ups    = ups[:len(nokeys)]
    downs  = downs[:len(nokeys)]
    nokeys = nokeys[:len(ups)]
    
    final_data = ups + downs + nokeys
    shuffle(final_data)
    #print(len(final_data))
    np.save('balanced_training_data-{}.npy'.format(i),final_data)
