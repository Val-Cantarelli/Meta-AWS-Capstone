from .base import *

DEBUG = True
ALLOWED_HOSTS = ["127.0.0.1", "localhost"]

STATICFILES_DIRS = [
    BASE_DIR / "ui_app" / "static",
]
print("Environment: Local Development")
API_BASE_URL = "http://localhost:8001"  # URL do backend local
