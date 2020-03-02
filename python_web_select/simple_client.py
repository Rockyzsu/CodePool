# coding: utf-8
"""
创建socket-----> 连接socket -------> 发送数据 -------> 接收数据
"""

from socket import socket, AF_INET, SOCK_STREAM

s = socket(AF_INET, SOCK_STREAM)
s.connect(('localhost', 8000))
s.send(b'hello')
res = s.recv(1024)
print(res)
