import tflite_runtime.interpreter as tflite

import os
from io import BytesIO
from urllib import request
from PIL import Image
import numpy as np

# Set the model name using an environment variable
MODEL_NAME = os.getenv("MODEL_NAME", "model_2024_hairstyle_v2.tflite")

interpreter = tflite.Interpreter(model_path = MODEL_NAME)
interpreter.allocate_tensors()
input_index = interpreter.get_input_details()[0]['index']
output_index = interpreter.get_output_details()[0]['index']

target_size = interpreter.get_input_details()[0]['shape']
target_size = target_size[1], target_size[2]

def download_image(url):
    # Open the URL, read the content and store it in a buffer (temporarily holding data in memory)
    with request.urlopen(url) as resp:
        buffer = resp.read()
    # Create a BytesIO stream from the buffer
    stream = BytesIO(buffer)
    # Open the stream as an Image object
    img = Image.open(stream)
    return img


def prepare_image(img, target_size):
    """Convert image to 'RGB' mode and resize it to the target size.

    Args:
        img: Image object to be converted and resized.
        target_size : A tuple (width, height) for the target size.

    Returns:
        The converted and resized image
    """
    if img.mode != 'RGB':
        img = img.convert('RGB')
    # Resize the image to the target size using the NEAREST filter
    img = img.resize(target_size, Image.NEAREST)
    return img

def predict(url):
    image = download_image(url)
    prepared_image = prepare_image(image, target_size)
    image_array = np.array(prepared_image, dtype=np.float32) / 255
    X = np.array([image_array])
    interpreter.set_tensor(input_index, X)
    interpreter.invoke()
    output_data = interpreter.get_tensor(output_index)
    return float(output_data[0])


def lambda_handler(event, context):
    url = event['url']
    pred = predict(url)
    result = {'prediction': pred}

    return result

def test():
    print("MODEL_NAME: ", MODEL_NAME)
    event = {'url': ' https://habrastorage.org/webt/yf/_d/ok/yf_dokzqy3vcritme8ggnzqlvwa.jpeg'}
    result = lambda_handler(event, context=None)
    print(result)
    
if __name__ == "__main__":
    test()