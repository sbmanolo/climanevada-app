"""
WSGI config for climanevada project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/howto/deployment/wsgi/
"""

import os, time, traceback, signal, sys
from django.core.wsgi import get_wsgi_application

sys.path.append("/var/www/climanevada")
sys.path.append("/var/www/climanevada/climanevada")

os.environ.setdefault("LANG", "en_US.UTF-8")
os.environ.setdefault("LC_ALL", "en_US.UTF-8")

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "climanevada.settings")

activate_this = '/home/iecolab/virtualenvs/clima/bin/activate_this.py'

exec(open(activate_this).read(), {'__file__': activate_this})

application = get_wsgi_application()
 