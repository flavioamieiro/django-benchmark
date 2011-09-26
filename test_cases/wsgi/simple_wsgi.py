from wsgiref.util import setup_testing_defaults
from wsgiref.simple_server import make_server

def hello_world(environ, start_response):
    setup_testing_defaults(environ)

    status = '200 OK'
    headers = [('Content-type', 'text/html')]

    start_response(status, headers)

    response_body = "simple wsgi example"
    return [response_body]

httpd = make_server('127.0.0.1', 8000, hello_world)
print "Listening on port 8000..."
httpd.serve_forever()
