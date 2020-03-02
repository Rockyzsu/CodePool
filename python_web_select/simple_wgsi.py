#coding=utf-8

import socket
import io
import sys

class WSGIServer(object):

    address_family = socket.AF_INET
    socket_type = socket.SOCK_STREAM
    request_queue_size = 1

    def __init__(self,server_address):
        # Create a listening socket
        self.listen_socket = listen_socket = socket.socket(self.address_family,self.socket_type)

        listen_socket.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
        listen_socket.bind(server_address)
        listen_socket.listen(self.request_queue_size)

        # Get server hostname and port
        host,port = self.listen_socket.getsockname()[:2]
        self.server_name = socket.getfqdn(host)
        self.server_port = port

        # Return headers set by Web Framework/Application
        self.headers_set = []

    def set_app(self,application):
        self.application = application

    def server_forever(self):
        listen_socket = self.listen_socket

        while True:
            self.client_connection,client_address = listen_socket.accept()
            self.handle_request()

    def handle_request(self):
        self.request_data = request_data = self.client_connection.recv(1024)

        print(''.join('<{line}\n'.format(line=line) for line in request_data.splitlines()))

        self.parse_request(request_data)

        #Construct environment
        env = self.get_envrion()

        result = self.application(env,self.start_response)

        self.finish_response(result)

    def parse_request(self,text):
        request_line = text.splitlines()[0]
        request_line = request_line.rstrip('\r\n')

        # Break down the request into components
        (self.request_method, # GET
         self.path,           # /hello
         self.version         # HTTP/1.1
        ) = request_line.split()

    def get_envrion(self):
        env ={}
        # Required WSGI variables
        env['wsgi.version'] = (1, 0)
        env['wsgi.url_scheme'] = 'http'
        env['wsgi.input'] = io.StringIO(self.request_data.decode('utf-8'))
        env['wsgi.errors'] = sys.stderr
        env['wsgi.multithread'] = False
        env['wsgi.multiprocess'] = False
        env['wsgi.run_once'] = False
        # Required CGI variables
        env['REQUEST_METHOD'] = self.request_method  # GET
        env['PATH_INFO'] = self.path  # /hello
        env['SERVER_NAME'] = self.server_name  # localhost
        env['SERVER_PORT'] = str(self.server_port)  # 8888

        return env

    # Add some headers
    def start_response(self,status,respons_headers,exc_info=None):
        server_headers = [
            ('Date','Tue,31 Mar 2015 12:54:58 GMT'),
            ('Server','WSGI Server 0.2')
        ]

        self.headers_set = [status,respons_headers + server_headers]

    def finish_response(self,result):
        try:
            status,response_headers = self.headers_set
            response = 'HTTP/1.1 {status}\r\n'.format(status=status)
            for head in response_headers:
                response += '{0}:{1}\r\n'.format(*head)
            response += '\r\n'

            for data in result:
                response += data

            print(''.join('>{line}\n'.format(line=line) for line in response.splitlines()))
            self.client_connection.sendall(response)
        finally:
            self.client_connection.close()

SERVER_ADDRESS = (HOST,PORT) = '',8000

def make_server(server_address,application):
    server = WSGIServer(server_address)
    server.set_app(application)
    return server

if __name__ == '__main__':
    if len(sys.argv) < 2:
        sys.exit('Provide a WSGI application object as module:callable')
    app_path = sys.argv[1]
    module,application = app_path.split(':')
    module = __import__(module)
    application = getattr(module,application)
    httpd = make_server(SERVER_ADDRESS,application)
    print('WSGIServer: Serving HTTP on port {port} ...'.format(port=PORT))
    httpd.server_forever()