from django.http import HttpResponse
from django.db import connection

def raw_connection(request):
    cursor = connection.cursor()

    cursor.close()

    return HttpResponse('Django has just created a cursor to the database.')
