from .base import *

print("Environment: Production")
DEBUG = True
ALLOWED_HOSTS = ["127.0.0.1", "localhost"]
# create and add domain
API_BASE_URL = os.getenv("API_BASE_URL", "https://6qpkzrhv4c.execute-api.us-east-1.amazonaws.com/v1")

STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"

SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
#(optional)SESSION_EXPIRE_AT_BROWSER_CLOSE = True