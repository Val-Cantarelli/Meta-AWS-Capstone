import os
import sys
import traceback

#sys.path.append(os.path.join(os.path.dirname(__file__), 'LittleLemon'))


print("sys.path:", sys.path)
print("cwd:", os.getcwd())
print("files:", os.listdir(os.getcwd()))

import os

def print_dir_tree(base_path, prefix=""):
    items = sorted(os.listdir(base_path))
    for i, item in enumerate(items):
        path = os.path.join(base_path, item)
        is_last = (i == len(items) - 1)
        connector = "└── " if is_last else "├── "
        print(f"{prefix}{connector}{item}")
        if os.path.isdir(path):
            new_prefix = prefix + ("    " if is_last else "│   ")
            print_dir_tree(path, new_prefix)

print("Conteúdo de /var/task/LittleLemon:")
print("LittleLemon/")
print_dir_tree("/var/task/LittleLemon", prefix="└── ")


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
