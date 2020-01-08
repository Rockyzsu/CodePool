import cv2
import base64
from io import BytesIO
import numpy as np
from PIL import Image
import pickle



def b64img_to_nparray(b64_img):
    buf = BytesIO(base64.decodebytes(b64_img.encode()))
    im = Image.open(buf)
    frame = np.asarray(im)
    return frame


def nparray_to_b64img(frame, convert_to_rgb=True):
    # encode the frame in JPEG format
    if convert_to_rgb:
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    (flag, encodedImage) = cv2.imencode(".jpg", frame)
    encodedImage = base64.encodebytes(bytearray(encodedImage)).decode('utf-8')
    return encodedImage
