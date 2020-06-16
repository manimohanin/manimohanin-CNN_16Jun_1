# -*- coding: utf-8 -*-
"""
Created on Sun Nov 17 11:39:40 2019

@author: 138410
"""
# autopep8 -i MessyOrNot_run.py
import glob

from distlib import logger

from djangoapp import settings
from keras import backend as K
from keras.models import load_model
#from tkinter import messagebox
from keras.preprocessing import image
import numpy as np
from utils import draw_boxes, load_class_names, load_images
from yolo_v3 import Yolo_v3
import tensorflow as tf
import os
import traceback

path = settings.MEDIA_ROOT
base_dir = settings.BASE_DIR
os.environ['CUDA_VISIBLE_DEVICES'] = '0'

dirpath = path + "/test/"

def get_test_filename():
    path = settings.MEDIA_ROOT
    dirpath = path + "/test/"
    fils = glob.glob(dirpath + '*.*')
    if fils:
        test_file = max(fils, key=os.path.getctime)
        base = os.path.basename(test_file)
        return dirpath + base

def delete_files():
    try:
        fles = glob.glob(dirpath + '*.*')
        for fl in fles:
            os.remove(fl)
    except OSError as e:
        print("Error: %s : %s" % (fl, e.strerror))

def messy_or_not():
    try:
        os.environ['CUDA_VISIBLE_DEVICES'] = '0'

        _MODEL_SIZE = (416, 416)
        _CLASS_NAMES_FILE = 'coco.names'
        _MAX_OUTPUT_SIZE = 50
        global detection_result
        detection_result = {}

        iou_threshold = 0.5
        confidence_threshold = 0.5
        filepath = get_test_filename()
        if not filepath:
            return 'Info: Test Image does not exist'
        input_names = filepath

        class_names = load_class_names(_CLASS_NAMES_FILE)
        n_classes = len(class_names)

        #import tensorflow.compat.v1 as tf1
        # tf.compat.disable_v2_behavior()

        # def main(iou_threshold, confidence_threshold, input_names):
        # model.save_weights(
        #    'E:/NTT DATA/CCE/CCE Codebase/Sentiment Analysis/SentimentAnalysis/MessyOrNot/model_saved.h5')
        #imagename = '0_qzQUpL-gOOSVKXbi.jpg'
        # serialize model to JSON
        #model_json = model.to_json()
        # load json and create model
        #json_file = open('model.json', 'r')
        #loaded_model_json = json_file.read()
        #json_file.close()
        #loaded_model = model_from_json(loaded_model_json)
        # load weights into new model
        #loaded_model.load_weights("/model_saved.h5")
        #loaded_model = load_model('trained_model.h5')

        model_path = path + '/model_saved/model_saved.h5'
        print('model_path=', model_path)
        loaded_model = load_model(model_path)
        #loaded_model.load_weights(checkpoint_path)
        print("Loaded model from disk")

        test_image = image.load_img(filepath, target_size=(224, 224))
        test_image = image.img_to_array(test_image)
        test_image = np.expand_dims(test_image, axis=0)
        result = loaded_model.predict(test_image)
        #labels = (train_generator.class_indices)
        #labels = dict((v, k) for k, v in labels.items())
        #predictions = [labels[k] for k in result]
        # list_clean = os.listdir(path_clean)  # dir is your directory path
        #number_files_clean = len(list_clean)+1
        # list_messy = os.listdir(path_messy)  # dir is your directory path
        #number_files_messy = len(list_messy)+1
        #messagebox.showinfo("MessyOrNot", "Testing")

        # object detection
        # Yolo v3 image detection
        model = Yolo_v3(n_classes=n_classes, model_size=_MODEL_SIZE,
                        max_output_size=_MAX_OUTPUT_SIZE,
                        iou_threshold=iou_threshold,
                        confidence_threshold=confidence_threshold)

        batch = load_images(input_names, model_size=_MODEL_SIZE)
        inputs = tf.placeholder(tf.float32, [1, *_MODEL_SIZE, 3])
        detections = model(inputs, training=False)
        saver = tf.train.Saver(tf.global_variables(scope='yolo_v3_model'))

        with tf.Session() as sess:
            saver.restore(sess, base_dir+ '/weights/model.ckpt')
            detection_result = sess.run(detections, feed_dict={inputs: batch})

        draw_boxes(input_names, detection_result, class_names, _MODEL_SIZE)

        print('Detections have been saved successfully.')

        class_count = []
        my_string = ""
        for cls in range(len(class_names)):
            class_count.append(len(detection_result[0][cls]))
            if len(detection_result[0][cls]) > 0:
                my_string = my_string + \
                    str(class_names[cls])+"-"+str(len(detection_result[0][cls]))+"\n"
        print(my_string)
        print(result)
        print(np.argmax(result[0]))
        pred_class = (np.argmax(result[0]))
        # user result display
        K.clear_session()
        if pred_class == 0:
            #messagebox.showinfo("MessyOrNot", "Clean " + "\n" + my_string)
            #delete_files(dirpath)
            return "Clean " + " -- "+ my_string
        if pred_class == 1:
            #messagebox.showinfo("MessyOrNot", "Messy " + "\n" + my_string)
            #delete_files(dirpath)
            return "Messy " + " -- " + my_string
        if pred_class == 2:
            #messagebox.showinfo("MessyOrNot", "Not a Conference Room " + "\n")
            #delete_files(dirpath)
            return "Not a Conference Room "
    except Exception as exc:
        logger.error(traceback.format_exc())
        print(traceback.format_exc())
    finally:
        K.clear_session()
