import time
from base_camera import BaseCamera
import cv2
cascPath = 'haarcascade_frontalface_dataset.xml'  # dataset
faceCascade = cv2.CascadeClassifier(cascPath)

class Camera(BaseCamera):
    """An emulated camera implementation that streams a repeated sequence of
    files 1.jpg, 2.jpg and 3.jpg at a rate of one frame per second."""
    imgs = [open(f + '.jpg', 'rb').read() for f in ['1', '2', '3']]

    # video = cv2.VideoCapture('mitmproxy.mp4')
    video = cv2.VideoCapture(0)
    # 对于mp4的视频无效
    video.set(cv2.CAP_PROP_FRAME_WIDTH,300)
    video.set(cv2.CAP_PROP_FRAME_HEIGHT,300)

    restart=False

    @staticmethod
    def frames_img():
        while True:
            time.sleep(0.1)
            yield Camera.imgs[int(time.time()) % 3]

    @staticmethod
    def frames_video():

        print('been call')
        if Camera.restart:
            Camera.video = cv2.VideoCapture(0)

        while True:

            ret,frame = Camera.video.read()
            if ret:
                # frame=cv2.transpose(frame)
                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            else:
                time.sleep(1)
                print('frame drop')
                break
            # 人脸识别
            faces = faceCascade.detectMultiScale(
                gray,
                scaleFactor=1.1,
                minNeighbors=5,
                minSize=(30, 30),
                flags=cv2.CASCADE_SCALE_IMAGE
            )

            # Draw a rectangle around the faces
            for (x, y, w, h) in faces:
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

            _,img = cv2.imencode('.jpg',frame)
            yield img.tobytes()


