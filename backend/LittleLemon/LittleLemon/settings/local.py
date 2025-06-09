from .base import *
from decouple import config


DEBUG = True
SECRET_KEY = config("SECRET_KEY")
ALLOWED_HOSTS = ["127.0.0.1", "localhost"]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': config('LOCAL_DB_NAME'),
        'USER': config('LOCAL_DB_USER'),
        'PASSWORD':config('LOCAL_DB_PASSWORD'),
        'HOST': "127.0.0.1",
        'PORT': 3306,
    }
}

SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(days=1),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=7),
    "ROTATE_REFRESH_TOKENS": False,
    "BLACKLIST_AFTER_ROTATION": False,
}

CSRF_COOKIE_SECURE = False
SESSION_COOKIE_SECURE = False