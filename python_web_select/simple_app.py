def simpleapp(envrion,start_response):
    HELLO = "Hello world!\n"
    status = '200 OK'
    response_headers = [('Content-type','text/plain')]
    start_response(status,response_headers)
    return [HELLO]
