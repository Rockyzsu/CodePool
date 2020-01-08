import requests
import time
import cv2
import imutils
#  for cctv camera'rtsp://username:password@ip_address:554/user=username_password='password'_channel=channel_number_stream=0.sdp'
#  example of cctv or rtsp: 'rtsp://mamun:123456@101.134.16.117:554/user=mamun_password=123456_channel=1_stream=0.sdp'

# video_capture = cv2.VideoCapture('video_20191218_144737.mp4')  # 0 for web camera live stream
import utils

src=0
# src = 'rtsp://admin:byb123456@192.168.1.65:554/Streaming/channels/1/'

video_capture = cv2.VideoCapture(src)  # 0 for web camera live stream

config = {
    "server_url": "192.168.10.97",
    "server_port": "9002"
}
server_url = "http://" + config["server_url"] + ":" + str(config["server_port"])+'/action/recog'
video_src='rtsp://admin:byb123456@192.168.1.65:554/Streaming/channels/1/'

def camera_stream():
    while True:
        # Capture frame-by-frame
        ret, frame = video_capture.read()  # 为啥我的笔记本卡在这里？ A：不能放在全局
        # print(f'ret -- {ret}')
        # print('get frame')

        if ret:
            h,w=frame.shape[:2]
            # frame=cv2.resize(frame, (int(w/3),int(h/3)), interpolation=cv2.INTER_AREA)
            print(h,w)
            imgBase64 = utils.nparray_to_b64img(frame)
            start = time.time()
            res = requests.post(server_url, json={'imgBase64': imgBase64})
            res = res.json()
            # print(res)
            end = time.time()
            # print("post time ", end - start)
            print(f"cls value {res.get('cls')}")
            result_img = utils.b64img_to_nparray(res["img"])
            cv2.putText(result_img,
                        "Action {} Score {}".format(res["cls"], res["score"]),
                        (10, 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 1.4, (0, 0, 255), 3,
                        lineType=cv2.LINE_AA)

        return cv2.imencode('.jpg', result_img)[1].tobytes()
