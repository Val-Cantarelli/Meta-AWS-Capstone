from .base import *
from decouple import config


DEBUG = True
SECRET_KEY = config("SECRET_KEY")
ALLOWED_HOSTS = ["127.0.0.1", "localhost"]

# Add drf-spectacular for local development
INSTALLED_APPS += ['drf_spectacular']

# Override REST_FRAMEWORK for OpenAPI schema
REST_FRAMEWORK = {
    **REST_FRAMEWORK,
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
}

# Spectacular settings
SPECTACULAR_SETTINGS = {
    'TITLE': 'Little Lemon API',
    'DESCRIPTION': 'Restaurant management system API',
    'VERSION': '1.0.0',
    'SERVE_INCLUDE_SCHEMA': False,
}

# Use SQLite for local development (simpler setup)
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Fallback to MySQL if needed (commented out)
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.mysql',
#         'NAME': config('LOCAL_DB_NAME'),
#         'USER': config('LOCAL_DB_USER'),
#         'PASSWORD': config('LOCAL_DB_PASSWORD'),
#         'HOST': "127.0.0.1",
#         'PORT': 3306,
#     }
# }

SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(days=1),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=7),
    "ROTATE_REFRESH_TOKENS": False,
    "BLACKLIST_AFTER_ROTATION": False,
}

CSRF_COOKIE_SECURE = False
SESSION_COOKIE_SECURE = False