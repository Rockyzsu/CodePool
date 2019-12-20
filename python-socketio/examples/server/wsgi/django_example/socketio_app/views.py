# set async_mode to 'threading', 'eventlet', 'gevent' or 'gevent_uwsgi' to
# force a mode else, the best mode is selected automatically from what's
# installed
async_mode = None

import os

from django.http import HttpResponse
import socketio

basedir = os.path.dirname(os.path.realpath(__file__))
sio = socketio.Server(async_mode=async_mode)
thread = None
# 这个是server端

def index(request):
    global thread
    print('thread的值')
    print(thread)
    if thread is None:
        print('为空')
        # 代码放入到后台，只运行一次
        thread = sio.start_background_task(background_thread)

    return HttpResponse(open(os.path.join(basedir, 'static/index.html')))


def background_thread():
    """Example of how to send server generated events to clients."""
    count = 0
    while True:
        sio.sleep(10)
        count += 1
        print('触发了在后台执行---')
        # 下面的是发给前端
        print('我的sio session是 ---- {}')
        sio.emit('my_response', {'data': 'Server generated event'},
                 )
        # 如果设置一个namespace ，那么前端可能会收不到


@sio.event
def my_event(sid, message):
    print('从浏览器前端触发了一个my_event, 建立连接的时候开始的')
    sio.emit('my_response', {'data': message['data']}, room=sid)


@sio.event
def my_broadcast_event(sid, message):
    print('收到一个广播请求')
    sio.emit('my_response', {'data': message['data']})


@sio.event
def join(sid, message):
    print('收到一个join请求')
    sio.enter_room(sid, message['room'])
    sio.emit('my_response', {'data': 'Entered room: ' + message['room']},
             room=sid)


@sio.event
def leave(sid, message):
    print('收到一个leave请求')

    sio.leave_room(sid, message['room'])
    sio.emit('my_response', {'data': 'Left room: ' + message['room']},
             room=sid)


@sio.event
def close_room(sid, message):
    print('收到一个close请求')

    sio.emit('my_response',
             {'data': 'Room ' + message['room'] + ' is closing.'},
             room=message['room'])
    sio.close_room(message['room'])


@sio.event
def my_room_event(sid, message):
    print('收到一个my room evnet 请求')
    sio.emit('my_response', {'data': message['data']}, room=message['room'])


@sio.event
def disconnect_request(sid):
    # 关闭了哦
    print('准备关闭连接')
    sio.disconnect(sid)


@sio.event
def connect(sid, environ):
    sio.emit('my_response', {'data': 'Connected', 'count': 0}, room=sid)


@sio.event
def disconnect(sid):
    print('Client disconnected')

