# -*- coding: utf-8 -*-
# website: http://30daydo.com
# @Time : 2020/1/11 18:34
# @File : python_client_.py

#client端
import socket
import struct
import os
import json

sk = socket.socket()
sk.connect(('127.0.0.1',8989))

dic = {'opt':'upload','filename':None,'filesize':None}
file = 'Zoo foo'
dic['filename'] = file
dic['filesize'] = 100
str_dic = json.dumps(dic)
len_dic = struct.pack('i',len(str_dic))#自动将字典字符的长度转换为4个bytes类型的长度
sk.send(len_dic+str_dic.encode('utf-8'))