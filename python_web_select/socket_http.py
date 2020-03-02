from socket import socket, AF_INET, SOCK_STREAM
from urllib.parse import urlparse

# 使用socket请求 网页，底层的写法
def get_url(url):
    url = urlparse(url)
    host = url.netloc
    path = url.path
    if path == '':
        path = '/'

    client = socket(AF_INET, SOCK_STREAM)
    client.connect((host, 80))

    client.send('GET {} HTTP/1.1\r\nHost:{}\r\nConnection:close\r\n\r\n'.format(path, host).encode('utf-8'))
    
    data = b''
    while True:
        b = client.recv(1024)
        if b:
            data += b
        else:
            break
    data = data.decode('utf-8')

    print(data)

    client.close()

get_url('http://www.baidu.com')