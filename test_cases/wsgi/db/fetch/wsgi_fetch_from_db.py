import psycopg2

from wsgiref.util import setup_testing_defaults
from wsgiref.simple_server import make_server


def fetch_from_db(environ, start_response):
    setup_testing_defaults(environ)

    status = '200 OK'
    headers = [('Content-type', 'text/html')]

    start_response(status, headers)

    connection = psycopg2.connect('dbname=test user=test')
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM test;")

    response_body = "id -> %03d; name -> %s" % cursor.fetchone()

    cursor.close()
    connection.close()

    return [response_body]

httpd = make_server('127.0.0.1', 8003, fetch_from_db)
print "Listening on port 8003..."
httpd.serve_forever()
