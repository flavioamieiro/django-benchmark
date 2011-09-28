from django.shortcuts import render_to_response

def response_from_disk(request):
    return render_to_response('response_from_disk.txt')
