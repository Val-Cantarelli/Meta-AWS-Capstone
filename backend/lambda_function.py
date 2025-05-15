import os
import sys
import traceback

import os


try:
    from LittleLemon.LittleLemon import utils
except Exception as e:
    print("Erro real ao importar utils:", e)
    traceback.print_exc()
    raise 

import django
from mangum import Mangum
ENV = os.getenv("DJANGO_ENV", "production")
os.environ.setdefault("DJANGO_SETTINGS_MODULE", f"LittleLemon.LittleLemon.settings.{ENV}")

import importlib
try:
    settings_module = f"LittleLemon.LittleLemon.settings.{ENV}"
    importlib.import_module(settings_module)
except Exception as e:
    print(f"Failed to import settings module: {settings_module}\n{e}")

# Keep it this import here!!
from LittleLemon.LittleLemon.asgi import application
django.setup()
handler = Mangum(application, lifespan="off")
