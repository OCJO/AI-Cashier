from torch.autograd import Variable
import torch
import cv2

from .yolo_utils import non_max_suppression, prep_image


def get_class_names(label_path):
    with open(label_path, 'rt') as f:
        classes = f.read().rstrip('\n').split('\n')
    classes.insert(0, '__background__')
    return classes if classes else None


class DetectBoxes:
    def __init__(self, label_path, conf_threshold=0.5, nms_threshold=0):
        self.classes = get_class_names(label_path)
        self.confThreshold = conf_threshold
        self.nmsThreshold = nms_threshold
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

    def bounding_box_yolo(self, frame, inp_dim, model):
        height, width, _ = frame.shape
        img, orig_im, dim = prep_image(frame, inp_dim)
        im_dim = torch.FloatTensor(dim).repeat(1, 2).to(self.device)
        img = img.to(self.device)

        input_imgs = Variable(img)

        with torch.no_grad():
            detections = model(input_imgs)
            detections = non_max_suppression(detections, self.confThreshold, self.nmsThreshold)

        detections = detections[0]
        formed_detection_data = []
        if detections is not None:
            im_dim = im_dim.repeat(detections.size(0), 1)
            scaling_factor = torch.min(inp_dim / im_dim, 1)[0].view(-1, 1)

            detections[:, [0, 2]] -= ((inp_dim - scaling_factor * im_dim[:, 0].view(-1, 1)) / 2).cpu()
            detections[:, [1, 3]] -= ((inp_dim - scaling_factor * im_dim[:, 1].view(-1, 1)) / 2).cpu()

            detections[:, 0:4] /= scaling_factor.cpu()

            for index, out in enumerate(detections):
                outs = out.tolist()
                left = int(outs[0]) if outs[0] > 0 else 0
                top = int(outs[1]) if outs[1] > 0 else 0
                right = int(outs[2]) if outs[2] < width else width
                bottom = int(outs[3]) if outs[3] < height else height

                cls = int(outs[-1])
                color = STANDARD_COLORS[(cls + 1) % len(STANDARD_COLORS)]

                self.draw_boxes(frame, self.classes[cls + 1], outs[4], left, top, right, bottom, color)
                formed_detection_data.append({
                    "object": self.classes[cls + 1],  # 인식된 객체
                    "accuracy": outs[4],  # 인식 정확도
                    "box": [left, top, right, bottom],  # Bounding Box 정보
                    "color": list(color)  # 색ID (R, G, B)
                })
        else:
            detections = []

        return frame, detections, formed_detection_data

    def draw_boxes(self, frame, class_id, score, left, top, right, bottom, color):
        txt_color = (0, 0, 0)
        if sum(color) < 500:
            txt_color = (255, 255, 255)

        cv2.rectangle(frame, (left, top), (right, bottom), color=color, thickness=2)

        label = '{}%'.format(round((score * 100), 1))
        if self.classes:
            label = ' %s %s ' % (class_id, label)

        label_size, base_line = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.4, 1)
        top = max(top, label_size[1])
        cv2.rectangle(frame, (left, top - round(1.5 * label_size[1])),
                      (left + round(1.5 * label_size[0]), top + base_line), color=color, thickness=cv2.FILLED)
        cv2.putText(frame, label, (left, top), cv2.FONT_HERSHEY_SIMPLEX, 0.6, color=txt_color, thickness=2)


""" Bounding Box - Color palette """
STANDARD_COLORS = [
    (255, 248, 240), (230, 224, 176), (0, 255, 127), (255, 255, 77), (180, 130, 70), (238, 130, 238),
    (212, 255, 127), (220, 220, 220), (255, 127, 0), (220, 245, 245), (196, 228, 255), (205, 222, 239),
    (135, 184, 222), (113, 104, 83), (255, 255, 255), (30, 105, 210), (80, 127, 255), (235, 206, 154),
    (220, 248, 255), (60, 20, 220), (255, 255, 0), (139, 139, 0), (32, 165, 218), (169, 169, 169),
    (107, 183, 189), (0, 140, 255), (214, 112, 218), (113, 179, 60), (192, 192, 192), (32, 165, 218),
    (255, 0, 255), (205, 90, 106), (96, 164, 244), (140, 180, 210), (250, 230, 230), (71, 99, 255),
    (87, 139, 46), (204, 209, 72), (0, 252, 124), (19, 69, 139), (222, 196, 176), (225, 105, 65),
    (0, 165, 255), (35, 142, 107), (92, 92, 205), (210, 250, 250), (225, 228, 228), (34, 139, 34),
    (255, 144, 30), (240, 255, 240), (211, 0, 148), (230, 240, 250), (0, 0, 255), (0, 255, 255),
    (128, 128, 0), (216, 191, 216), (60, 141, 224), (0, 230, 238), (77, 66, 102), (75, 0, 217),
    (149, 104, 83), (0, 179, 255), (112, 208, 60), (19, 17, 123), (195, 120, 136), (143, 10, 18),
    (220, 80, 96), (81, 218, 11), (67, 130, 255), (101, 195, 116), (0, 0, 128), (251, 195, 115),
    (165, 103, 0), (238, 104, 123), (135, 220, 201), (154, 250, 0), (280, 84, 0), (59, 69, 24),
    (93, 236, 178), (94, 247, 252)
]
# 126
# STANDARD_COLORS = [
#     'AliceBlue', 'Chartreuse', 'Aqua', 'Aquamarine', 'Azure', 'Beige', 'Bisque',
#     'BlanchedAlmond', 'BlueViolet', 'BurlyWood', 'CadetBlue', 'AntiqueWhite',
#     'Chocolate', 'Coral', 'CornflowerBlue', 'Cornsilk', 'Crimson', 'Cyan',
#     'DarkCyan', 'DarkGoldenRod', 'DarkGrey', 'DarkKhaki', 'DarkOrange',
#     'DarkOrchid', 'DarkSalmon', 'DarkSeaGreen', 'DarkTurquoise', 'DarkViolet',
#     'DeepPink', 'DeepSkyBlue', 'DodgerBlue', 'FireBrick', 'FloralWhite',
#     'ForestGreen', 'Fuchsia', 'Gainsboro', 'GhostWhite', 'Gold', 'GoldenRod',
#     'Salmon', 'Tan', 'HoneyDew', 'HotPink', 'IndianRed', 'Ivory', 'Khaki',
#     'Lavender', 'LavenderBlush', 'LawnGreen', 'LemonChiffon', 'LightBlue',
#     'LightCoral', 'LightCyan', 'LightGoldenRodYellow', 'LightGray', 'LightGrey',
#     'LightGreen', 'LightPink', 'LightSalmon', 'LightSeaGreen', 'LightSkyBlue',
#     'LightSlateGray', 'LightSlateGrey', 'LightSteelBlue', 'LightYellow', 'Lime',
#     'LimeGreen', 'Linen', 'Magenta', 'MediumAquaMarine', 'MediumOrchid',
#     'MediumPurple', 'MediumSeaGreen', 'MediumSlateBlue', 'MediumSpringGreen',
#     'MediumTurquoise', 'MediumVioletRed', 'MintCream', 'MistyRose', 'Moccasin',
#     'NavajoWhite', 'OldLace', 'Olive', 'OliveDrab', 'Orange', 'OrangeRed',
#     'Orchid', 'PaleGoldenRod', 'PaleGreen', 'PaleTurquoise', 'PaleVioletRed',
#     'PapayaWhip', 'PeachPuff', 'Peru', 'Pink', 'Plum', 'PowderBlue', 'Purple',
#     'Red', 'RosyBrown', 'RoyalBlue', 'SaddleBrown', 'Green', 'SandyBrown',
#     'SeaGreen', 'SeaShell', 'Sienna', 'Silver', 'SkyBlue', 'SlateBlue',
#     'SlateGray', 'SlateGrey', 'Snow', 'SpringGreen', 'SteelBlue', 'GreenYellow',
#     'Teal', 'Thistle', 'Tomato', 'Turquoise', 'Violet', 'Wheat', 'White',
#     'WhiteSmoke', 'Yellow', 'YellowGreen'
# ]
