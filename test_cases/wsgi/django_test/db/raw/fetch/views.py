from django.http import HttpResponse
from django.db import connection

def raw_fetch(request):
    cursor = connection.cursor()

    cursor.execute('SELECT * from db_pythonbrasil')
    row = cursor.fetchone()
    cursor.close()

    return HttpResponse('Django fetched from database without the ORM: PythonBrasil[%d] was in %s' % row)
