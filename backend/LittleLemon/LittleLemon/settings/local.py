from .base import *

DEBUG = True
ALLOWED_HOSTS = ["127.0.0.1", "localhost"]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'mysqlRDS_littlelemon',  
        'USER': 'root',
        'PASSWORD': 'database',  
        'HOST': '127.0.0.1',  
        'PORT': '3306',
    }
}

SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=15),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=7),
    "ROTATE_REFRESH_TOKENS": True,  
    "BLACKLIST_AFTER_ROTATION": True,
}

CSRF_COOKIE_SECURE = False
SESSION_COOKIE_SECURE = False
