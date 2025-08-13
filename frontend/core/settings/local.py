from .base import *
import os

DEBUG = True
ALLOWED_HOSTS = ["127.0.0.1", "localhost"]


CSRF_TRUSTED_ORIGINS = ["http://127.0.0.1:8000", "http://localhost:8000", "https://localhost:8443","https://127.0.0.1:8443"]

SECURE_SSL_REDIRECT = False
SESSION_COOKIE_SECURE = False
CSRF_COOKIE_SECURE = False
SECURE_HSTS_SECONDS = 0
SECURE_PROXY_SSL_HEADER = None


STATICFILES_DIRS = [
    BASE_DIR / "ui_app" / "static",
]
print("Environment: Local Development")
API_BASE_URL = os.environ.get("API_BASE_URL", "http://127.0.0.1:8001")

