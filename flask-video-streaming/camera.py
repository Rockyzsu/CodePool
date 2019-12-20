import time
from base_camera import BaseCamera
import cv2

class Camera(BaseCamera):
    """An emulated camera implementation that streams a repeated sequence of
    files 1.jpg, 2.jpg and 3.jpg at a rate of one frame per second."""
    imgs = [open(f + '.jpg', 'rb').read() for f in ['1', '2', '3']]

    video = cv2.VideoCapture('mitmproxy.mp4')
    # 对于mp4的视频无效
    video.set(cv2.CAP_PROP_FRAME_WIDTH,100)
    video.set(cv2.CAP_PROP_FRAME_HEIGHT,100)

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
            Camera.video = cv2.VideoCapture('video_20191218_144737.mp4')

        while True:

            ret,frame = Camera.video.read()
            if ret:
                _,img = cv2.imencode('.jpg',frame)
                yield img.tobytes()

            else:
                time.sleep(1)
                print('i am sleep')
                # continue
                Camera.restart=True
                break

