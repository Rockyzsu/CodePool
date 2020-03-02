# coding: utf-8
"""
这个文件只是一个简单的示例说明，不能够运行
"""
def run_application(application):
    # Server Code
    # This is where an application/framework stores an HTTP status
    # and HTTP response headers for server to transmit to the client
    headers_set = []
    # Environment dictionary with WSGI
    environ = {}

    def start_response(status, response_headers, exc_info=None):
        headers_set[:] = [status, response_headers]

    # Server invoke the "application" callable and get back the response body
    result = application(environ, start_response)


def app(environ, start_response):
    """A barebones WSGI app."""
    start_response('200 OK', [('Content-Type', 'text/plain')])
    return ['Hello world']

run_application(app)