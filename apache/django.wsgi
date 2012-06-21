import site
site.addsitedir('/home/opendap/cmipstatusenv/lib/python2.6/site-packages')

import os
import sys

os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'

import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()

site_root = '/home/opendap/cmipsite' #adjust to the server!
path = site_root
if path not in sys.path:
    sys.path.append(path)
