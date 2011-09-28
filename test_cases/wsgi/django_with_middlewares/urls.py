from django.conf.urls.defaults import patterns, include, url
from direct_response.views import direct_response
from response_from_disk.views import response_from_disk
from db.raw.connect.views import raw_connection
from db.raw.fetch.views import raw_fetch
from db.orm.fetch.views import orm_fetch

urlpatterns = patterns('^/wsgi/django_with_middlewares/',
    url('direct_response/$', direct_response),
    url('response_from_disk/$', response_from_disk),
    url('db/raw/connect/$', raw_connection),
    url('db/raw/fetch/$', raw_fetch),
    url('db/orm/fetch/$', orm_fetch),
)
