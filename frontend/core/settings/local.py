from .base import *

DEBUG = True
ALLOWED_HOSTS = ["127.0.0.1", "localhost"]

STATICFILES_DIRS = [
    BASE_DIR / "ui_app" / "static",
]
print("Environment: Local Development")
API_BASE_URL='https://6qpkzrhv4c.execute-api.us-east-1.amazonaws.com/v1'
