from datetime import timedelta

DEBUG = True

ALLOWED_HOSTS = ["127.0.0.1", "localhost"]

SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=1),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=7),
    "ROTATE_REFRESH_TOKENS": True,  
    "BLACKLIST_AFTER_ROTATION": True,
}


CSRF_COOKIE_SECURE = False
SESSION_COOKIE_SECURE = False
