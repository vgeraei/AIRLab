"""
WSGI config for AIRLab project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.10/howto/deployment/wsgi/
"""

import os,sys

from django.core.wsgi import get_wsgi_application

sys.path.append('/home/pi/Desktop/django/AIRLab')

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "AIRLab.settings")

application = get_wsgi_application()

