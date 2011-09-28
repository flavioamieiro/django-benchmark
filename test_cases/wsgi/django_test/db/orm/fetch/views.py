from django.http import HttpResponse
from db.models import PythonBrasil

def orm_fetch(request):
    python_brasil = PythonBrasil.objects.get(id=1)
    return HttpResponse('Django got this from the database with the ORM: PythonBrasil[%d] was in %s' % (python_brasil.id, python_brasil.place))
