from __future__ import print_function

from collections import OrderedDict
from getpass import getpass
from os import linesep
from os.path import join

from django.utils.crypto import get_random_string

from fabric.api import task
from fabric.colors import green

from . import PROJECT_ROOT


def write_settings(settings_file, target, settings):
    with open(settings_file, 'w+') as of:
        print('# Generated by Fabric setup task', file=of)
        print(linesep, file=of)
        print(
            'from {{ project_name }}.config.{} import *'.format(target),
            file=of
        )
        print(linesep, file=of)
        for k, v in settings.iteritems():
            print("{} = '{}'".format(k, v), file=of)


@task()
def local_setup():
    "Generate {{ project_name }}/settings.py"
    target = 'development'
    settings = OrderedDict()
    settings['SECRET_KEY'] = get_random_string(54)
    settings['DATABASES__DEFAULT__PASSWORD'] = getpass('PostgreSQL Password: ')
    settings['POSTMARK_API_KEY'] = getpass('Postmark API Key: ')
    local_settings = join(PROJECT_ROOT, 'settings.py')
    write_settings(local_settings, target, settings)
    print(green('{} generated'.format(local_settings)))
