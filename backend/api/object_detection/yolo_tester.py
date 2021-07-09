import time
import cv2
import torch
import os
import yaml

from .modeling_darknet import Darknet
from .draw_detection_boxes import DetectBoxes

# added import
import numpy as np
import PIL
import json
import argparse

from torchvision import transforms
from PIL import Image


class YOLO:
    def __init__(self, property):
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

        print("Loading YOLO network.....")
        model = Darknet(property['config_file'], img_size=property['resol']).to(self.device)
        model.load_darknet_weights(property['weight_file'])
        model.eval()
        print("Network successfully loaded")

        self.model = model

        self.label_path = property['labels']
        self.conf = property['conf']  # conf : Confidence threshold for predictions
        self.nms = property['nms']  # nms : NMS threshold
        self.resol = property['resol']  # resol : Resolution of network. Higher increases accuracy but decreases speed

    def object_detection(self, image_path, output_dir):
        # load detection class, default confidence threshold is 0.5
        detect = DetectBoxes(self.label_path, conf_threshold=self.conf, nms_threshold=self.nms)
        
        try:
            # Read Image file
            image = cv2.imread(image_path, cv2.IMREAD_COLOR)   
        except IOError:
            print("Cannot read Input image file -", image_path)
            return 0, 0
        
        start = time.time()
        image, detections, formed_detection_data = detect.bounding_box_yolo(image, self.resol, self.model)
        end = time.time()

        cv2.putText(image, '{:.2f}ms'.format((end - start) * 1000), (40, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.75,
                    (255, 0, 0), 2)

        objects = []
        
        cv2.imwrite(output_dir, image)
        
        if detections is not None:
            detect_data = [d.tolist() for d in detections]
            for d in detect_data:
                objects.append(int(d[6]))
            return image, objects
        else:
            return image, objects
