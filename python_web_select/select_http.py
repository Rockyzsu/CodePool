"""
select + 回调 + 事件循环
"""

from selectors import DefaultSelector, EVENT_WRITE, EVENT_READ
from urllib.parse import urlparse
from socket import socket, AF_INET, SOCK_STREAM


selector = DefaultSelector()

class Fetcher:
    def get_content(self, key):
        res = self.client.recv(1024)
        if res:
            self.data += res
        else:
            selector.unregister(key.fd)
            data = self.data.decode('utf-8')
            print(data)
            self.client.close()
            

    def send_content(self, key):
        selector.unregister(key.fd)
        self.client.send('GET {} HTTP/1.1\r\nHost:{}\r\nConnection:close\r\n\r\n'.format(self.path, self.host).encode('utf-8'))
        selector.register(self.client.fileno(), EVENT_READ, self.get_content)

    def get_html(self, url):
        url = urlparse(url)
        self.host = url.netloc
        self.path = url.path
        if self.path == '':
            self.path = '/'

        self.data = b''
        self.client = socket(AF_INET, SOCK_STREAM)
        self.client.setblocking(False)
        try:
            self.client.connect((self.host, 80))
        except BlockingIOError:
            pass  
        # 注册这个事件，就绪后进行回调
        selector.register(self.client.fileno(), EVENT_WRITE, self.send_content)

def loop():
    while True:
        ready = selector.select()
        for key, mask in ready:
            callback = key.data
            callback(key)


if __name__ == "__main__":
    f = Fetcher()
    f.get_html('http://www.baidu.com')
    loop()