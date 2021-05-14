"""
Run a rest API exposing the yolov5s object detection model
"""
import argparse
import io
import json
import os

import cv2
from PIL import Image
from flask import Flask, request
import numpy as np
import torch

from yolov5.models.experimental import attempt_load
from yolov5.utils.datasets import letterbox
from yolov5.utils.general import check_img_size, non_max_suppression, scale_coords

import logging

# Model Parameters
WEIGHTS = os.path.join(os.path.dirname(__file__), 'weights.pt')
IMGSZ = 704
CONF_THRESH = 0.4  # Object confidence threshold
IOU_THRESH = 0.45  # IOU threshold for NMS
NMS_CLASSES = None  # Class filter for NMS
AGNOSTIC_NMS = False  # Class agnostic NMS
CLASS_MAP = ['boats']

# Hardware Parameters
DEVICE = 'cpu'


def load_model(weights=WEIGHTS, device=DEVICE, imgsz=IMGSZ):
    """ Load the YoloV5 model. """
    model = attempt_load(weights, map_location=device)
    stride = int(model.stride.max())
    imgsz = check_img_size(imgsz, s=stride)
    return (model, stride, imgsz)


def preprocess(image_file, stride, imgsz):
    """ Prepare the input for inferencing. """
    # read image file
    img = np.asarray(bytearray(image_file), dtype="uint8")
    img = cv2.imdecode(img, 1)
    imgsz0 = torch.Tensor(img.shape[:2])

    # resize image
    img = letterbox(img, imgsz, stride=stride)[0]

    # convert from BGR to RGB
    img = img[:, :, ::-1].transpose(2, 0, 1)
    img = np.ascontiguousarray(img)

    # convert to tensor
    img = torch.from_numpy(img).to(DEVICE)

    # normalize RGB values to percentage
    img = img.float() / 255.0
    if img.ndimension() == 3:
        img = img.unsqueeze(0)

    return img, imgsz0

def new_preprocess(img, stride, imgsz):
    """ Prepare the input for inferencing. """
    # read image file
    # img = np.asarray(bytearray(image_file), dtype="uint8")
    # img = cv2.imdecode(img, 1)
    # img = img_in.astype(np.uint8)
    imgsz0 = torch.Tensor(img.shape[:2])

    # resize image
    img = letterbox(img, imgsz, stride=stride)[0]
    
    # convert from BGR to RGB
    img = img[:, :, ::-1].transpose(2, 0, 1)
    img = np.ascontiguousarray(img)

    # convert to tensor
    img = torch.from_numpy(img).to(DEVICE)

    # normalize RGB values to percentage
    img = img.float() / 255.0
    if img.ndimension() == 3:
        img = img.unsqueeze(0)

    return img, imgsz0

def new_detect(img_file, model, stride, imgsz):
    # preprocess image
    logging.debug(f'img_file: shape = {img_file.shape}, dtype: {img_file.dtype}')
    img, imgsz0 = new_preprocess(img_file, stride, imgsz)

    # run inferencing
    pred = model(img)[0]
    pred = non_max_suppression(pred, CONF_THRESH, IOU_THRESH, NMS_CLASSES, agnostic=AGNOSTIC_NMS)[0]

    # postprocess results
    pred = postprocess(pred, imgsz0, img.shape[2:])

    # return the results
    return {'objects': pred}

def postprocess(predictions, imgsz0, imgsz1):
    """ Convert class IDs to class names. """
    predictions[:, :4] = scale_coords(imgsz1, predictions[:, :4], imgsz0).round()
    predictions = predictions.cpu().numpy().tolist()
    return [{"box": row[:4],
             "confidence": row[4],
             "class": CLASS_MAP[int(row[5])]} for row in predictions]


def detect(img_file, model, stride, imgsz):
    # preprocess image
    img, imgsz0 = preprocess(img_file, stride, imgsz)

    # run inferencing
    pred = model(img)[0]
    pred = non_max_suppression(pred, CONF_THRESH, IOU_THRESH, NMS_CLASSES, agnostic=AGNOSTIC_NMS)[0]

    # postprocess results
    pred = postprocess(pred, imgsz0, img.shape[2:])

    # return the results
    return {'objects': pred}

class Detection:
    def __init__(self):
        pass

    def load(self):
        #
        # Load model from storage. Called by Seldon.
        #
        home = os.environ['HOME']
        weights = f'{home}/weights.pt'
        weights = f'./weights.pt'
        logging.info(f'pytorch version: {torch.__version__}')
        logging.info(f'Loading model file: {weights}')

        IMGSZ = 704
        DEVICE = 'cpu'
        (model, stride, imgsz) = load_model(weights, DEVICE, IMGSZ)
        self._model = model
        self._stride = stride
        self._imgsz = imgsz
        self._model_loaded = True
        logging.info(f'Model {weights} loaded, stride = {stride}, image size = {imgsz}')
        pass

    def predict(self, X, features_names=None, **kwargs):
        if not self._model_loaded:
            self.load()
        logging.debug(f'predict(): input X, shape = {X.shape}, type = {type(X)}.')
        logging.debug(f'X: shape = {X.shape}, dtype: {X.dtype}')
        
        #
        # Insure the input is of type uint8 or OpenCV will crash.
        #
        img = X.astype(np.uint8)

        #
        # Hardcoded prediction using test image (for debugging).
        # 
        # filename = os.path.abspath('./boats.png')
        # img_bytes = open(filename, "rb").read()
        # img = np.asarray(bytearray(img_bytes), dtype="uint8")
        # img = cv2.imdecode(img, 1)
        # prediction = new_detect(img, self._model, self._stride, self._imgsz)
        # logging.debug(f'img: shape = {img.shape}, dtype: {img.dtype}')
        # logging.debug(f'predict(): hardcoded prediction: {prediction}')
        
        #
        # Prediction using input X
        #
        prediction = new_detect(img, self._model, self._stride, self._imgsz)
        logging.debug(f'predict(): RESTprediction: {prediction}')

        return prediction
