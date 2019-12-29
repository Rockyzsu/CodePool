#!/usr/bin/env python
from importlib import import_module
import os
from flask import Flask, render_template, Response,request

# import camera driver

from camera import Camera

# Raspberry Pi camera module (requires picamera package)
# from camera_pi import Camera

app = Flask(__name__)

# 这个程序可以同时运行几个客户端
# c=Camera()
@app.route('/')
def index():
    """Video streaming home page."""
    # print('call')
    # print(request)
    ip = request.remote_addr
    print(f'===== {ip} ======')
    return render_template('index.html')


def gen(camera):
    """Video streaming generator function."""
    # 进来了就是一个死循环
    while True:
        frame = camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')


@app.route('/video_feed')
def video_feed():
    """Video streaming route. Put this in the src attribute of an img tag."""
    return Response(gen(Camera()),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


if __name__ == '__main__':
    app.run(host='0.0.0.0', threaded=True,port=80,debug=False)
