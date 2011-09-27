import psycopg2

from wsgiref.util import setup_testing_defaults
from wsgiref.simple_server import make_server


def connect_to_db(environ, start_response):
    setup_testing_defaults(environ)

    status = '200 OK'
    headers = [('Content-type', 'text/html')]

    start_response(status, headers)

    connection = psycopg2.connect('dbname=test user=test')

    connection.close()

    response_body = "I've just connected to the database!"

    return [response_body]

httpd = make_server('127.0.0.1', 8002, connect_to_db)
print "Listening on port 8002..."
httpd.serve_forever()
