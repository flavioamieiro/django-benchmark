from django.conf.urls.defaults import patterns, include, url
from direct_response.views import direct_response

urlpatterns = patterns('^/wsgi/django_test/',
    url('direct_response/$', direct_response),
)
