import os

from wsgiref.util import setup_testing_defaults
from wsgiref.simple_server import make_server

response_file_path = os.path.join(os.path.dirname(__file__), 'response.txt')

def read_from_disk(environ, start_response):
    setup_testing_defaults(environ)

    status = '200 OK'
    headers = [('Content-type', 'text/html')]

    start_response(status, headers)

    with open(response_file_path, 'r') as f:
        response_body = f.read()

    return [response_body]

httpd = make_server('127.0.0.1', 8001, read_from_disk)
print "Listening on port 8001..."
httpd.serve_forever()
