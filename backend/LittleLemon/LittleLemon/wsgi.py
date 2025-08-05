
import os

from django.core.wsgi import get_wsgi_application

ENV = os.getenv("DJANGO_ENV", "production")  

os.environ.setdefault("DJANGO_SETTINGS_MODULE", f"LittleLemon.settings.{ENV}")

application = get_wsgi_application()
