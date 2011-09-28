# -*- encoding: utf-8 -*-
import os
import datetime
from fabric.api import run, put, sudo, local, cd, settings, get

# Sempre executa o fabric no diretório raiz do repositório
os.chdir(os.path.dirname(__file__))


REMOTE_ROOT = '/srv/load_testing'
CONFIG_DIR = REMOTE_ROOT + '/config'
NGINX_CONFIG = CONFIG_DIR + '/load_testing.vhost'

def benchmark(url, base_filename, requests=100000, concurrency=1000):
    filename = '{0}-{1}'.format(datetime.datetime.now().strftime('%Y%m%d_%H-%M-%S'), base_filename)
    remote_file_path = os.path.join('/tmp', filename)
    local_file_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'data', filename)

    run('ab -n {requests} -c {concurrency} {url} > {remote_file_path}'.format(**locals()))
    get(remote_file_path, local_file_path)
    run('rm {0}'.format(remote_file_path))

def benchmark_all():
    base_url = 'http://192.168.132.97'
    test_cases = [
        ('/static_html/index.html', 'static_html'),
        ('/wsgi/simple_wsgi.py', 'simple_wsgi'),
        ('/wsgi/disk_read/wsgi_read_from_disk.py', 'wsgi_read_from_disk'),
        ('/wsgi/db/connect/wsgi_connect_to_db.py', 'wsgi_connect_to_db'),
        ('/wsgi/db/fetch/wsgi_fetch_from_db.py', 'wsgi_fetch_from_db'),
        ('/wsgi/django_test/direct_response/', 'django_direct_response'),
        ('/wsgi/django_test/response_from_disk/', 'django_response_from_disk'),
        ('/wsgi/django_test/db/raw/connect/', 'django_db_raw_connect'),
        ('/wsgi/django_test/db/raw/fetch/', 'django_db_raw_fetch'),
        ('/wsgi/django_test/db/orm/fetch/', 'django_db_orm_fetch'),
    ]

    for path, name in test_cases:
        url = '{0}{1}'.format(base_url, path)
        filename = '{0}.txt'.format(name)
        benchmark(url, filename)

def deploy(revision):
    local_archive_path = remote_archive_path = _create_git_archive(revision)

    put(local_archive_path, remote_archive_path)
    run('tar jxf %s -C %s' % (remote_archive_path, REMOTE_ROOT))
    run('rm -v %s' % remote_archive_path)
    sudo('ln -f -s %s /etc/nginx/sites-enabled/001-load_testing' % NGINX_CONFIG)

    create_upstart_job('simple_wsgi')
    create_upstart_job('wsgi_read_from_disk')
    create_upstart_job('wsgi_connect_to_db')
    create_upstart_job('wsgi_fetch_from_db')
    create_upstart_job('django')

    sudo('/etc/init.d/nginx restart')
    sudo("init Q")
    run('/usr/bin/python %s/test_cases/wsgi/django_test/manage.py syncdb' % REMOTE_ROOT)

    reload_server('simple_wsgi')
    reload_server('wsgi_read_from_disk')
    reload_server('wsgi_connect_to_db')
    reload_server('wsgi_fetch_from_db')
    reload_server('django')



def _create_git_archive(revision):
    rev = local('git rev-parse %s' % revision, capture=True)
    archive_path = '/tmp/%s.tar.bz2' % rev

    local('git archive --format=tar %s | bzip2 -c > %s' % (rev, archive_path))

    return archive_path

def reload_server(name):
    with settings(warn_only=True):
        sudo('initctl stop %s' % name)
    sudo('initctl start %s' % name)

def create_upstart_job(name):
    with cd('/etc/init/'):
        sudo('cp -f %s/%s.conf %s.conf' % (CONFIG_DIR, name, name))
