# You must keep this file if you plan to use WSGI servers for production (such as Gunicorn or uWSGI) or other synchronous environments. It is critical for production deployments of Django.

"""
WSGI config for chatdb project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'chatdb.settings')

application = get_wsgi_application()
