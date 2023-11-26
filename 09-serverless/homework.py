#!/usr/bin/env python
#coding: utf-8

import os
import numpy as np

# import tensorflow.lite as tflite
import tflite_runtime.interpreter as tflite

from io import BytesIO
from urllib import request

from PIL import Image

# Set the model name using an environment variable or default to "bees-wasps.tflite"
MODEL_NAME = os.getenv("MODEL_NAME", "bees-wasps.tflite")

def download_image(url):
    # Download image from the provided URL
    with request.urlopen(url) as resp:
        buffer = resp.read()
    stream = BytesIO(buffer)
    img = Image.open(stream)
    return img

def prepare_image(img, target_size):
    # Ensure the image is in RGB mode and resize to the target size
    if img.mode != 'RGB':
        img = img.convert('RGB')
    img = img.resize(target_size, Image.NEAREST)
    return img

def prepare_input(x):
    # Normalize input values to be in the range [0, 1]
    return x / 255.0

# Load the TFLite model and allocate tensors
interpreter = tflite.Interpreter(model_path=MODEL_NAME)
interpreter.allocate_tensors()

# Get input and output tensor indices
input_index = interpreter.get_input_details()[0]['index']
output_index = interpreter.get_output_details()[0]['index']

def predict(url):
    # Predict the class based on the input image URL
    img = download_image(url)
    img = prepare_image(img, target_size=(150, 150))

    x = np.array(img, dtype='float32')
    X = np.array([x])
    X = prepare_input(X)

    # Set input tensor and invoke the interpreter
    interpreter.set_tensor(input_index, X)
    interpreter.invoke()

    # Get the predictions from the output tensor
    preds = interpreter.get_tensor(output_index)

    return float(preds[0, 0])

def lambda_handler(event, context):
    # Lambda function handler to predict based on the provided event (URL)
    url = event['url']
    pred = predict(url)
    result = {
        'prediction': pred
    }

    return result

def test():
    print("MODEL_NAME: ", MODEL_NAME)
    event = {'url': 'https://habrastorage.org/webt/rt/d9/dh/rtd9dhsmhwrdezeldzoqgijdg8a.jpeg'}
    result = lambda_handler(event, context=None)
    print(result)
    
if __name__ == "__main__":
    test()