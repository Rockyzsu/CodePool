# -*- coding: utf-8 -*-
# website: http://30daydo.com
# @Time : 2020/1/11 14:26
# @File : client.py

import socket
import os
import sys
import struct

import cv2
import pickle


def socket_client():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect(('localhost',23456))
    except socket.error as msg:
        print(msg)
        sys.exit(1)

    # print(s.recv(1024))

    while 1:
        filepath = input("please input file path: ")
        # if os.path.isfile(filepath):
            # 定义定义文件信息。128s表示文件名为128bytes长，l表示一个int或log文件类型，在此为文件大小
            # fileinfo_size = struct.calcsize('128sl')
            # 定义文件头信息，包含文件名和文件大小
            # fhead = struct.pack('128sl', bytes(os.path.basename(filepath).encode('utf-8')),os.stat(filepath).st_size)
            # s.send(fhead)
            # print ('client filepath: {0}'.format(filepath))
        frame = cv2.imread(filepath)
        if frame is None:
            print(' not read the file')
        frame_pickle = pickle.dumps(frame)

        print(len(frame_pickle))
        print(type(frame_pickle))

        frame_len = len(frame_pickle)

        # fp = open(filepath, 'rb')
        # while 1:
        #     data = fp.read(1024)
        #     if not data:
        #         print ('{0} file send over...'.format(filepath))
        #         break
        l=struct.pack('i',frame_len)
        print(l)
        s.send(l)
        s.send(frame_pickle)


if __name__ == '__main__':
    socket_client()
