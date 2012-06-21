import site
site_root = '/home/opendap/cmipsite' #adjust to the server!
virtualenv_root = '/home/opendap/cmipstatusenv' #adjust to the server!
site.addsitedir(os.path.join(virtualenv_root, '/lib/python2.6/site-packages'))

import os
import sys

os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'

import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()

import settings
path = site_root
if path not in sys.path:
    sys.path.append(path)
