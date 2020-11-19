import sys
import argparse
from .yolo import YOLO, detect_video
from PIL import Image
import matplotlib.pyplot as plt


def detect_img(yolo, image_pathname, image_out_pathname):
    print("-"*100)
    print(yolo)
    print(yolo.__dict__)
    print("-"*100)
    image = Image.open(image_pathname)
    r_image = yolo.detect_image(image)
    r_image.show()
    r_image.save(image_out_pathname)

def init_fun(root):
    model_path= root + "/model_data/trained_weights_stage_1.h5"
    classes_path= root + "/model_data/_classes.txt"
    anchors_path= root + "/model_data/yolo_anchors.txt"
    yolo_ins = YOLO(**{'classes_path': classes_path, 'image': True, 'output': '', 'input': './path2your_video', 'model_path': model_path, 'anchors_path': anchors_path})
    return yolo_ins

if __name__ == '__main__':
    detect_img(init_fun('.'), './scripts/test/3.jpg', './scripts/test/z.jpg')
