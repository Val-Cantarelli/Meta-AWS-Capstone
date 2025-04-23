from .base import *

DEBUG = True
ALLOWED_HOSTS = ["127.0.0.1", "localhost"]

STATICFILES_DIRS = [
    BASE_DIR / "ui_app" / "static",
]
print("hello local")
# Segurança desativada apenas para desenvolvimento
CSRF_COOKIE_SECURE = False
SESSION_COOKIE_SECURE = False
