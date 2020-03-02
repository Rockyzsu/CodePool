# coding: utf-8
"""
wsgi的流程

  +--------------------+         +------------+         +----------------+       +--------+
 /创建一个socket，监听 /  -----> /获取请求数据 /  -----> /回调application / ----> /返回数据 /
+--------------------+         +------------+         +---------------+        +--------+

WSGI的environment存储了请求的方法，路径等关键信息
start_response 作为回调函数，在application运行的时候，做一些动作
"""


import socket
import io
import sys


class WSGIServer:
    address_family = socket.AF_INET
    socket_type = socket.SOCK_STREAM
    request_queue_size = 1

    def __init__(self, server_address):
        # Create a listening socket
        self.listen_socket = listen_socket = socket.socket(
            self.address_family,
            self.socket_type
        )
        # Allow to reuse the same address
        listen_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        # Bind
        listen_socket.bind(server_address)
        # Listen
        listen_socket.listen(self.request_queue_size)
        # Get Server host name and port
        host, port = self.listen_socket.getsockname()[:2]
        self.server_name = socket.getfqdn(host)
        self.server_port = port
        # Return headers set by Web framework/Web application

    def set_app(self, application):
        self.application = application

    def server_forever(self):
        listen_socket = self.listen_socket
        while True:
            # New client connection
            self.client_connection, client_address = listen_socket.accept()
            # Handle one request and close the client connection, Then loop
            # over to wait for another client connection
            self.handle_one_request()

    def handle_one_request(self):
        self.request_data = request_data = self.client_connection.recv(1024)
        # Print request data
        print(''.join('< {line}\n'.format(line=line) for line in request_data.splitlines()))

        self.parse_request(request_data)

        # Construct environment dictionary using request data
        env = self.get_environ()

        # call our application callable and get back a result that will become Http response body
        result = self.application(env, self.start_response)

        # Construct a response and send it back to client
        self.finish_response(result)

    def parse_request(self, text):
        request_line = text.splitlines()[0]
        request_line = request_line.rstrip('\r\n')
        # Break down request line into component
        (self.request_method, self.path, self.request_version) = request_line.split()

    def get_environ(self):
        env = {}
        # Required variables
        env['wsgi.version'] = (1, 0)
        env['wsgi.url_scheme'] = 'http'
        env['wsgi.input'] = io.StringIO(self.request_data)
        env['wsgi.errors'] = sys.stderr
        env['wsgi.multithread'] = False
        env['wsgi.multiprocess'] = False
        env['wsgi.run_once'] = False
        # Required CGI variables
        env['REQUEST_METHOD'] = self.request_method  # GET
        env['PATH_INFO'] = self.path  # /hello
        env['SERVER_NAME'] = self.server_name  # localhost
        env['SERVER_PORT'] = str(self.server_port)  # 8000
        return env

    def start_response(self, status, response_headers, exc_info=None):
        # Add necessary server headers
        server_headers = [
            ('Date', 'Tue, 31 Mar 2015 12:54:48 GMT'),
            ('Server', 'WSGIServer 0.2'),
        ]
        self.headers_set = [status, response_headers + server_headers]

    def finish_response(self, result):
        try:
            status, response_headers = self.headers_set
            response = 'HTTP/1.1 {status}\r\n'.format(status=status)
            for header in response_headers:
                response += '{}: {}\r\n'.format(*header)
            response += '\r\n'
            for data in result:
                response += data
            # print formatted data
            print(''.join('> {line}\n'.format(line=line) for line in response.splitlines()))
            self.client_connection.sendall(response)
        finally:
            self.client_connection.close()


SERVER_ADDRESS = (HOST, PORT) = '', 8000


def make_server(server_address, application):
    server = WSGIServer(server_address)
    server.set_app(application)
    return server


if __name__ == '__main__':
    if len(sys.argv) < 2:
        sys.exit('Provide a WSGI application object as module:callable')
    app_path = sys.argv[1]
    module, application = app_path.split(':')
    module = __import__(module)
    application = getattr(module, application)
    httpd = make_server(SERVER_ADDRESS, application)
    print('WSGIServer: Server HTTP on port {port}...\n'.format(port=PORT))
    httpd.server_forever()
