import site
import ..settings
import os.path
site.addsitedir(os.path.join(settings.server_configs['virtualenv_home'], '/lib/python2.6/site-packages'))

import os
import sys

os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'

import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()

import settings
path = settings['site_root']
if path not in sys.path:
    sys.path.append(path)
