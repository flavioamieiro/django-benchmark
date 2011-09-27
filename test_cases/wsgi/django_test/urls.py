from django.conf.urls.defaults import patterns, include, url
from direct_response.views import direct_response
from response_from_disk.views import response_from_disk

urlpatterns = patterns('^/wsgi/django_test/',
    url('direct_response/$', direct_response),
    url('response_from_disk/$', response_from_disk),
)
