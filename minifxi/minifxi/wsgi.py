"""
WSGI config for minifxi project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/2.2/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

#os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'minifxi.settings')  # grcl4 -> -- Deplyed 21.04.2021
#application = get_wsgi_application()



os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'minifxi.settings.local')  # grcl4 -> ++ Deplyed 21.04.2021
#os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'minifxi.settings.production')  # grcl4 -> ++ Deplyed 21.04.2021
#from dj_static import Cling

#application = Cling(get_wsgi_application())

application = get_wsgi_application()

