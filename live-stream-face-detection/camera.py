import time
import cv2

#  for cctv camera'rtsp://username:password@ip_address:554/user=username_password='password'_channel=channel_number_stream=0.sdp'
#  example of cctv or rtsp: 'rtsp://mamun:123456@101.134.16.117:554/user=mamun_password=123456_channel=1_stream=0.sdp'

# video_capture = cv2.VideoCapture('video_20191218_144737.mp4')  # 0 for web camera live stream
cascPath = 'haarcascade_frontalface_dataset.xml'  # dataset
faceCascade = cv2.CascadeClassifier(cascPath)

src=0
rtsp = 'rtsp://admin:byb123456@192.168.1.64:554/Streaming/channels/1/'

video_capture = cv2.VideoCapture(src)  # 0 for web camera live stream
print(video_capture.isOpened())

def camera_stream():

    while True:
        # Capture frame-by-frame
        ret, frame = video_capture.read() # 为啥我的笔记本卡在这里？ A：不能放在全局
        print(f'ret -- {ret}')
        print('get frame')
        # if ret:
            # frame=cv2.transpose(frame)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        # else:
        #     time.sleep(1)
        #     print('frame drop')
        #     break
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

            # Display the resulting frame in browser
        return cv2.imencode('.jpg', frame)[1].tobytes()
