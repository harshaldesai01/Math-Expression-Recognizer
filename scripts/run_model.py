import os
import json
import keras
import numpy as np
import matplotlib.pyplot as plt
from keras.models import Sequential
from keras.layers import Conv2D
from keras.layers import MaxPooling2D
from keras.layers import Dense
from keras.layers import Flatten
from keras.layers import Dropout
from keras.layers import BatchNormalization
from training_monitor import TrainingMonitor
# fix random seed for reproducibility
seed = 7
numpy.random.seed(seed)

path_to_train_data = /path_to_train_data/


from tensorflow.keras.preprocessing.image import ImageDataGenerator

train_datagen = ImageDataGenerator(rescale = 1./255,
                                   shear_range = 0.2,
                                   zoom_range = 0.2, validation_split=0.2)

#test_datagen = ImageDataGenerator(rescale = 1./255)

training_set = train_datagen.flow_from_directory(path_to_train_data,
                                                 target_size = (32, 32),
                                                 batch_size = 128,
                                                 class_mode ='categorical', subset='training')
validation_set = train_datagen.flow_from_directory(path_to_train_data,
                                                 target_size = (32, 32),
                                                 batch_size = 128,
                                                 class_mode ='categorical', subset='validation')

classifier = Sequential()
classifier.add(Conv2D(64, (3, 3), padding='same', input_shape = (32, 32, 3), activation = 'relu'))
classifier.add(MaxPooling2D(pool_size = (2, 2)))
classifier.add(BatchNormalization())
classifier.add(Conv2D(64, (3, 3),padding='same',  activation = 'relu'))
classifier.add(MaxPooling2D(pool_size = (2, 2)))
classifier.add(Conv2D(128, kernel_size=5, padding='same', activation='relu'))
classifier.add(BatchNormalization())
classifier.add(Conv2D(128, kernel_size=5, padding='same', activation='relu'))
classifier.add(BatchNormalization())
classifier.add(MaxPooling2D(pool_size =2, strides=2))
classifier.add(Flatten())
classifier.add(Dense(1024, activation='relu'))
classifier.add(BatchNormalization())
classifier.add(Dropout(0.5))
classifier.add(Dense(units = 128, activation = 'relu'))
classifier.add(Dense(units = 75, activation = 'softmax'))
classifier.summary()
classifier.compile(optimizer=keras.optimizers.Adam(lr=1e-3), loss='categorical_crossentropy', metrics=['accuracy'])
#Adding Checkpoint and early stopping callbacks

figPath = os.path.sep.join([r'/path_to_snaps/snaps', "{}.png".format(os.getpid())])
jsonPath = os.path.sep.join([r'/path_to_snaps/models', "{}.json".format(os.getpid()+1)])
path_checkpoint = 'hack_checkpoint_2.keras'
callback_checkpoint=keras.callbacks.callbacks.ModelCheckpoint(filepath=path_checkpoint, monitor='val_loss', verbose=1, save_weights_only=True, save_best_only=True)
callback_early_stopping = keras.callbacks.callbacks.EarlyStopping(monitor='val_loss', patience=5, verbose=1)
callback_reduce_lr = keras.callbacks.callbacks.ReduceLROnPlateau(monitor='val_loss', factor=0.1, min_lr=1e-5, patience=0, verbose=1)
callbacks= [TrainingMonitor(figPath, jsonPath=jsonPath), callback_early_stopping, callback_checkpoint, callback_reduce_lr]

classifier.fit_generator(training_set, validation_data =validation_set, epochs = 25, callbacks=callbacks)
