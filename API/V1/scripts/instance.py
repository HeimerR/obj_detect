import sys
import argparse
from .yolo import YOLO, detect_video
from PIL import Image
import matplotlib.pyplot as plt

import os
from google.cloud import storage

from PIL import Image
import requests
from io import BytesIO

# Configure this environment variable via app.yaml
CLOUD_STORAGE_BUCKET = os.environ['CLOUD_STORAGE_BUCKET']
# CLOUD_STORAGE_BUCKET = 'yolo_data' # for local test

def detect_img(yolo, image_url, name):
    print("-"*100)
    print(yolo)
    print(yolo.__dict__)
    print("-"*100)
    response = requests.get(image_url)
    image = Image.open(BytesIO(response.content))
    
    r_image = yolo.detect_image(image)
    # Creating the "string" object to use upload_from_string
    img_byte_array = BytesIO()
    r_image.save(img_byte_array, format='JPEG')
    # Create a Cloud Storage client.
    gcs = storage.Client()

    # Get the bucket that the file will be uploaded to.
    bucket = gcs.get_bucket(CLOUD_STORAGE_BUCKET)

    # Create a new blob and upload the file's content.
    blob = bucket.blob(name + ".analized.jpg")

    blob.upload_from_string(img_byte_array.getvalue(), content_type="image/jpeg")

    # The public URL can be used to directly access the uploaded file via HTTP.
    return blob.public_url

def init_fun(root):
    model_path= root + "/model_data/trained_weights_stage_1.h5"
    classes_path= root + "/model_data/_classes.txt"
    anchors_path= root + "/model_data/yolo_anchors.txt"
    yolo_ins = YOLO(**{'classes_path': classes_path,
                       'image': True,
                       'output': '',
                       'input': './path2your_video',
                       'model_path': model_path,
                       'anchors_path': anchors_path})
    return yolo_ins

if __name__ == '__main__':
    detect_img(init_fun('.'), './scripts/test/3.jpg', './scripts/test/z.jpg') # for testing local storage
