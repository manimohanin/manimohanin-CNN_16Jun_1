from azure.storage.blob import BlockBlobService
from distlib import logger

from djangoapp import settings
import logging
from keras import backend as K
from keras.layers import Activation, Dropout, Flatten, Dense
from keras.layers import Conv2D, MaxPooling2D
from keras.models import Sequential
from keras.preprocessing.image import ImageDataGenerator
import os, shutil, glob
from datetime import datetime
import warnings
import tensorflow as tf
import traceback

path = settings.MEDIA_ROOT
warnings.filterwarnings('ignore')
start = datetime.now()
img_width, img_height = 224, 224
train_data_dir = path + "/train/"
validation_data_dir = path + "/validate/"
train_ckpt_dir = path + "/train_ckpt/"
model_path = path + "/model_saved/"

def create_model(input_shape):
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
    return model

def move_images_to_validate():
    for txt_file in glob.glob(validation_data_dir + "clean/*.*"):
        dest = txt_file.replace('/validate/', '/train/')
        shutil.move(txt_file, dest);
    for txt_file in glob.glob(validation_data_dir + "messy/*.*"):
        dest = txt_file.replace('/validate/', '/train/')
        shutil.move(txt_file, dest);
    for txt_file in glob.glob(validation_data_dir + "notcr/*.*"):
        dest = txt_file.replace('/validate/', '/train/')
        shutil.move(txt_file, dest);

def train_conf_model():
    try:
        nb_train_samples = sum([len(files) for r, d, files in os.walk(train_data_dir)])
        nb_validation_samples = sum([len(files) for r, d, files in os.walk(validation_data_dir)])
        print('nb_train_samples=',nb_train_samples)
        print('nb_validation_samples=', nb_validation_samples)
        if nb_train_samples == 0:
            print("No Image in Train directory")
            return "No Image in Train directory"
        if nb_validation_samples == 0:
            print("No Image in Test directory")
            return "No Image in Test directory"
        epochs = 20
        batch_size = 1
        if nb_validation_samples > 5:
            batch_size = 5
        print(nb_train_samples)
        print(nb_validation_samples)
        os.environ['CUDA_VISIBLE_DEVICES'] = '0'
        iou_threshold = 0.5
        confidence_threshold = 0.5
        if K.image_data_format() == 'channels_first':
            input_shape = (3, img_width, img_height)
        else:
            input_shape = (img_width, img_height, 3)

        model_ckpt = create_model(input_shape)

        # Display the model's architecture
        # model_ckpt.summary()

        # Specify the path where the checkpoint files will be stored
        checkpoint_path = train_ckpt_dir + "cp.ckpt"
        checkpoint_dir = os.path.dirname(checkpoint_path)
        # print(checkpoint_dir)

        # Loads the weights
        dirContents = os.listdir(checkpoint_dir)
        if len(dirContents) == 0:
            print('No model to restore')
        else:
            model_ckpt.load_weights(checkpoint_path)

        # Create a callback that saves the model's weights
        cp_callback = tf.keras.callbacks.ModelCheckpoint(
            filepath=checkpoint_path, save_best_only=True, save_weights_only=False, verbose=1)

        # data generator
        train_datagen = ImageDataGenerator(
            rescale=1. / 255,
            shear_range=0.2,
            zoom_range=0.2,
            horizontal_flip=True)

        test_datagen = ImageDataGenerator(rescale=1. / 255)

        train_generator = train_datagen.flow_from_directory(train_data_dir,
                                                            target_size=(
                                                                img_width, img_height),
                                                            batch_size=batch_size, class_mode='categorical')

        validation_generator = test_datagen.flow_from_directory(
            validation_data_dir,
            target_size=(img_width, img_height),
            batch_size=batch_size, class_mode='categorical')

        # Train the model with the new callback
        # Pass callback to training
        model_ckpt.fit_generator(train_generator,
                                 steps_per_epoch=nb_train_samples // batch_size,
                                 epochs=epochs, validation_data=validation_generator,
                                 validation_steps=nb_validation_samples // batch_size,
                                 callbacks=[cp_callback])

        # Save the weights
        # model_ckpt.save_weights('./checkpoints/my_checkpoint')

        loss, acc = model_ckpt.evaluate_generator(generator=validation_generator, steps=nb_validation_samples // batch_size)
        print("Restored model, accuracy: {:5.2f}%".format(100 * acc))

        # Create a basic model instance
        model = create_model(input_shape)
        # Evaluate the model
        loss, acc = model.evaluate_generator(generator=validation_generator, steps=nb_validation_samples // batch_size)
        print("Untrained model, accuracy: {:5.2f}%".format(100 * acc))

        model_ckpt.save(model_path + 'model_saved.h5')
        K.clear_session()
        del model_ckpt
        print("Saved model to disk")
    except Exception as exc:
        logger.error(traceback.format_exc())
        print(traceback.format_exc())
        move_images_to_validate()
        return "Failed"
    move_images_to_validate()
    return "Success"

