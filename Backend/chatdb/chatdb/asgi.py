"""
ASGI config for chatdb project.

The asgi.py file is used to configure Asynchronous Server Gateway Interface (ASGI) for your Django project. ASGI is a standard interface between web servers and Python web applications or frameworks, like Django. It supports asynchronous communication, which is particularly useful for handling WebSockets, long-lived connections, and other real-time communication mechanisms.
"""

import os

from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'chatdb.settings')

application = get_asgi_application()
