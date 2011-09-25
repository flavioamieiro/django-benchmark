# -*- encoding: utf-8 -*-
import os
from fabric.api import run, put, sudo, local

# Sempre executa o fabric no diretório raiz do repositório
os.chdir(os.path.dirname(__file__))


REMOTE_ROOT = '/srv/load_testing'
NGINX_CONFIG = REMOTE_ROOT + '/config/load_testing.conf'

def deploy(revision):
    local_archive_path = remote_archive_path = _create_git_archive(revision)

    put(local_archive_path, remote_archive_path)
    run('tar jxf %s -C %s' % (remote_archive_path, REMOTE_ROOT))
    run('rm -v %s' % remote_archive_path)
    sudo('ln -f -s %s /etc/nginx/sites-enabled/001-load_testing.conf' % NGINX_CONFIG)
    sudo ('/etc/init.d/nginx restart')


def _create_git_archive(revision):
    rev = local('git rev-parse %s' % revision, capture=True)
    archive_path = '/tmp/%s.tar.bz2' % rev

    local('git archive --format=tar %s | bzip2 -c > %s' % (rev, archive_path))

    return archive_path
