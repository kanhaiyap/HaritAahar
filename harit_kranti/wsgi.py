"""
WSGI config for harit_kranti project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application
from django.core.management import call_command

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "harit_kranti.settings")

application = get_wsgi_application()


def application(environ, start_response):
    # Run the import_products command
    try:
        call_command('import_products')
        print("Products imported successfully.")
    except Exception as e:
        print(f"Error importing products: {e}")

    return get_wsgi_application()(environ, start_response)