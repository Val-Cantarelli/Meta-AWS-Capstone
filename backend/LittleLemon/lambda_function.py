
import os
import django
from aws_lambda_wsgi import make_lambda_handler
from LittleLemon.wsgi import application

# Define o ambiente padrão para produção, igual ao wsgi.py
ENV = os.getenv("DJANGO_ENV", "production")  
os.environ.setdefault("DJANGO_SETTINGS_MODULE", f"LittleLemon.settings.{ENV}")

django.setup()

handler = make_lambda_handler(application)
