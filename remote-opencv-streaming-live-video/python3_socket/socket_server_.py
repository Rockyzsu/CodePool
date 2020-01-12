# -*- coding: utf-8 -*-
# website: http://30daydo.com
# @Time : 2020/1/11 18:34
# @File : socket_server_.py
import socket
import struct
import json
import os

sk = socket.socket()
sk.bind(('127.0.0.1',8989))
sk.listen()
conn,addr = sk.accept()

len_dic = struct.unpack('i',conn.recv(4))[0]#unpack解包接受的是元组类型,索引为0是字典的长度
print(len_dic)
str_dic = conn.recv(len_dic).decode('utf-8')#根据字典的长度将字典接收为字符串类型
dic = json.loads(str_dic)#将字符串类型的字典转换为字典(dict)
print(dic)
