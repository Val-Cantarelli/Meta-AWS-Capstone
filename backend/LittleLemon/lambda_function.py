import os
import django
from aws_lambda_wsgi import make_lambda_handler

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'LittleLemon.settings')
django.setup()

# Cria o manipulador Lambda com o WSGI
handler = make_lambda_handler()
