import os

from django.core.wsgi import get_wsgi_application

# gunicorn config.wsgi:application
os.environ.setdefault(
    "DJANGO_SETTINGS_MODULE",
    "config.settings",
)


application = get_wsgi_application()