from .base import *

DEBUG = True
#ALLOWED_HOSTS = ["127.0.0.1", "localhost"]

STATIC_URL = '/static/'

# Segurança desativada apenas para desenvolvimento
CSRF_COOKIE_SECURE = False
SESSION_COOKIE_SECURE = False
