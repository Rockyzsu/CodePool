# -*- coding: utf-8 -*-
# website: http://30daydo.com
# @Time : 2020/1/11 14:26
# @File : server.py

import socket
import threading
import time
import sys
import os
import struct
import numpy as np
import cv2
import pickle

def socket_service():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind(('localhost', 23456))#这里换上自己的ip和端口
        s.listen(10)
    except socket.error as msg:
        print(msg)
        sys.exit(1)
    print ("Waiting...")

    while 1:
        conn, addr = s.accept()
        t = threading.Thread(target=deal_data, args=(conn, addr))
        t.start()

def deal_data(conn, addr):
    print ('Accept new connection from {0}'.format(addr))
    while 1:
        # fileinfo_size = struct.calcsize('128sl')
        # buf = conn.recv(fileinfo_size)
        frame_size = conn.recv(4)

        if frame_size:
            # filename, filesize = struct.unpack('128sl', buf)
            # fn = filename.strip(str.encode('\00'))
            # new_filename = os.path.join(str.encode('./'), str.encode('new_') + fn)
            # print ('file new name is {0}, filesize if {1}'.format(new_filename, filesize))

            recvd_size = 0  # 定义已接收文件的大小
            # fp = open(new_filename, 'wb')
            print ("start receiving...")
            size = struct.unpack('i',frame_size)[0]
            f = conn.recv(size)
            fr=pickle.loads(f)
            # while not recvd_size == filesize:
            #     if filesize - recvd_size > 1024:
            #         data = conn.recv(1024)
            #         recvd_size += len(data)
            #     else:
            #         data = conn.recv(filesize - recvd_size)
            #         recvd_size = filesize
            #     datas+=data

                # fp.write(data)
            # frame = np.frombuffer(fp,dtype=np.int32)
            # print('data len')
            # print(len(datas))
            # frame = pickle.loads(datas)

            cv2.imwrite('test.jpg',fr)
            # cv2.imshow('frame',frame)
            # cv2.waitKey(10)
            # fp.close()
            print ("end receive...")
        conn.close()
        break


if __name__ == '__main__':
    socket_service()