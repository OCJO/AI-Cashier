import time
import cv2
import torch
import os
import yaml

from modeling_darknet import Darknet
from draw_detection_boxes import DetectBoxes

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
        result_image_path = output_dir + "/" + image_path.split("/")[1]
        cv2.imwrite(result_image_path, image)

        if detections is not None:
            detect_data = [d.tolist() for d in detections]
            for d in detect_data:
                objects.append(int(d[6]))
            return image, objects
        else:
            return image, objects


if __name__ == "__main__":
    # 해당 파일에서 직접 실행할 경우, import 에러가 발생할 수 있습니다
    #   (경로상 api.object_detection ... 으로 작성되어 생긴 오류)
    # 서버 동작시엔 environments.yaml 파일 내 세팅을 참조하여 동작
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    with open(f'{BASE_DIR}/model_property/model_environments.yaml', 'r', encoding='UTF8') as f:
        model_environment = yaml.load(f, Loader=yaml.FullLoader)

    yolov3_property = model_environment['yolov3_model']

    model_property = dict({
        "config_file": "output/customed_yolov3.cfg",
        "weight_file": "model_property/yolo-model-10.weights",
        "labels": "model_property/object.tags",
        "conf": 0.6,  # conf : Confidence threshold for predictions
        "nms": 0.4,  # nms : NMS threshold
        "resol": 416  # resol : Resolution of network. Higher increases accuracy but decreases speed
    })

    # 데이터셋에 맞는 클래스 수를 입력
    custom_classes = yolov3_property['classes']
    custom_filters = (custom_classes + 5) * 3

    custom_property = dict({
        "classes": custom_classes,
        "filters": custom_filters
    })
    yolo = YOLO(model_property)

    test_image_name = "test_data_mix.jpg"  # Test 대상 이미지 파일이름

    # '이미지 경로' 를 넣으면 OD 바운딩 박스가 그려진 이미지 데이터와 검출된 객체의 정보를 return
    image, detect_data = yolo.object_detection("test_image/" + test_image_name, "output")  # 테스트 이미지의 하위 경로와 위에 있는 파일이름
    print(detect_data)
    # 처리한 이미지 저장
    cv2.imshow("output", image)
    cv2.waitKey(0)
