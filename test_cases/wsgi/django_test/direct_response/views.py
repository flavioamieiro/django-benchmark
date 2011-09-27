from django.http import HttpResponse

def direct_response(request):
    return HttpResponse('hard-coded HttpResponse')
