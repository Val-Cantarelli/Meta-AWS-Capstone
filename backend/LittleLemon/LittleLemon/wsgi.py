
'''import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'LittleLemon.settings')

application = get_wsgi_application()
'''

import os

from django.core.wsgi import get_wsgi_application

# Define o ambiente padrão caso não esteja configurado
ENV = os.getenv("DJANGO_ENV", "production")  

os.environ.setdefault("DJANGO_SETTINGS_MODULE", f"LittleLemon.settings.{ENV}")

application = get_wsgi_application()
