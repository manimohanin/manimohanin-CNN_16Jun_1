from azure.storage.blob import BlockBlobService

from djangoapp.settings import AZURE_ACCOUNT_NAME, AZURE_ACCOUNT_KEY, AZURE_CONTAINER

from keras import backend as K
from keras.layers import Activation, Dropout, Flatten, Dense
from keras.layers import Conv2D, MaxPooling2D
from keras.models import Sequential
from keras.preprocessing.image import ImageDataGenerator
from tkinter import messagebox
from keras.preprocessing import image
import numpy as np

import sys
import tensorflow as tf
import os
import tkinter as tk
from tkinter import filedialog
import cv2
from datetime import datetime
import warnings
import traceback


def train_conf_model():
    try:
        warnings.filterwarnings('ignore')
        start = datetime.now()
        img_width, img_height = 224, 224
        train_data_dir = "D:/temp/media/train/"
        validation_data_dir = "D:/temp/media/test/"
        path_clean = "D:/temp/media/train/clean/"
        path_messy = "D:/temp/media/train/messy/"
        path_notcr = "D:/temp/media/train/notcr/"
        nb_train_samples = sum([len(files) for r, d, files in os.walk(train_data_dir)])
        nb_validation_samples = sum([len(files) for r, d, files in os.walk(validation_data_dir)])
        epochs = 20
        batch_size = 1
        os.environ['CUDA_VISIBLE_DEVICES'] = '0'
        # import tensorflow.compat.v1 as tf1
        # tf.compat.disable_v2_behavior()
        # def main(iou_threshold, confidence_threshold, input_names):
        iou_threshold = 0.5
        confidence_threshold = 0.5
        # input_names = filepath
        # class_names = load_class_names(_CLASS_NAMES_FILE)
        # n_classes = len(class_names)
        if K.image_data_format() == 'channels_first':
            input_shape = (3, img_width, img_height)
        else:
            input_shape = (img_width, img_height, 3)
        model = Sequential()
        model.add(Conv2D(32, (2, 2), input_shape=input_shape))
        model.add(Activation('relu'))
        model.add(MaxPooling2D(pool_size=(2, 2)))
        model.add(Conv2D(32, (2, 2)))
        model.add(Activation('relu'))
        model.add(MaxPooling2D(pool_size=(2, 2)))
        model.add(Conv2D(64, (2, 2)))
        model.add(Activation('relu'))
        model.add(MaxPooling2D(pool_size=(2, 2)))
        model.add(Flatten())
        model.add(Dense(64))
        model.add(Activation('relu'))
        model.add(Dropout(0.5))
        model.add(Dense(3))
        model.add(Activation('softmax'))
        model.compile(loss='categorical_crossentropy',
                      optimizer='rmsprop',
                      metrics=['accuracy'])
        train_datagen = ImageDataGenerator(
            rescale=1. / 255,
            shear_range=0.2,
            zoom_range=0.2,
            horizontal_flip=True)
        test_datagen = ImageDataGenerator(rescale=1. / 255)
        train_generator = train_datagen.flow_from_directory(train_data_dir,
                                                            target_size=(img_width, img_height),
                                                            batch_size=batch_size,
                                                            class_mode='categorical')
        validation_generator = test_datagen.flow_from_directory(
            validation_data_dir,
            target_size=(img_width, img_height),
            batch_size=batch_size, class_mode='categorical')
        print('fit_generator- START')
        model.fit_generator(train_generator,
                            steps_per_epoch=nb_train_samples // batch_size,
                            epochs=epochs, validation_data=validation_generator,
                            validation_steps=nb_validation_samples // batch_size)
        model.save_weights('D:/temp/media/MessyOrNot/model_saved.h5')
        print('fit_generator- END')
        # serialize model to JSON
        model_json = model.to_json()
        with open("model.json", "w") as json_file:
            json_file.write(model_json)
        # serialize weights to HDF5
        model.save_weights(
            'model_saved.h5')
        print("Saved model to disk")
        print("Process Time=", datetime.now() - start)
        # imagename = '0_qzQUpL-gOOSVKXbi.jpg'
        return 0
    except Exception as exc:
        print(traceback.format_exc())
    return 1
