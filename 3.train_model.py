from tensorflow.keras.models import Sequential, load_model
from tensorflow.keras.utils import to_categorical
from tensorflow.keras.layers import Dense, Dropout, Flatten
from tensorflow.keras.layers import Conv2D, MaxPooling2D
from tensorflow.keras import backend as K
from tensorflow.keras import optimizers

import time
import numpy as np
import cv2
from random import shuffle
from tensorflow.keras.callbacks import TensorBoard

batch_size = 256
num_classes = 3
epochs = 30

img_rows, img_cols = 16, 45

x = []
y = []
for i in range(1,8+1):
    train_data = np.load('balanced_training_data-{}.npy'.format(i))
    for data in train_data:
        image = data[0]
        key = data[1]
        x.append(image)
        y.append(key)
        
X = np.array(x)
y = np.array(y)

X = X.reshape(X.shape[0], img_rows, img_cols, 1)
input_shape = (img_rows, img_cols, 1)
y = y.reshape(-1,3)

print('X shape:', X.shape)
print(X.shape[0], 'train samples')

try:
    print("Load previous model!!")
    model = load_model("Dino.model")
except:
    print("No previous model!!")

model = Sequential()

model.add(Conv2D(256, kernel_size=(4,4), activation='relu', input_shape=input_shape))
model.add(MaxPooling2D(pool_size=(2,2)))
model.add(Dropout(0.5))
model.add(Flatten())

model.add(Dense(64, activation='relu'))
model.add(Dropout(0.25))

model.add(Dense(num_classes, activation='softmax'))

tensorboard = TensorBoard(log_dir="logs/{}-{}".format(batch_size,int(time.time())))

sgd = optimizers.SGD(lr=0.01, decay=1e-6, momentum=0.9, nesterov=True)
model.compile(loss='mean_squared_error',
              optimizer= sgd,
              metrics=['accuracy'])

model.fit(X, y, batch_size=batch_size, epochs=epochs,validation_split=0,callbacks=[tensorboard])

model.save('Dino.model')
##time.sleep(5)
##for i in range(len(X)):
##    cv2.imshow('test',X[i])
##    if cv2.waitKey(25) & 0xFF == ord('q'):
##        cv2.destroyAllWindows()
##        break

