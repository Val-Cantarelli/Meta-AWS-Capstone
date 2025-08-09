from .base import *
import os


DEBUG = False

ALLOWED_HOSTS = ["127.0.0.1", "localhost", "littlelemon-env.eba-gpgijkvt.us-east-1.elasticbeanstalk.com",".elasticbeanstalk.com", "vahltech.com", "www.vahltech.com"]  

API_BASE_URL = os.environ.get("API_BASE_URL")
SECRET_KEY = os.environ.get("DJANGO_SECRET_KEY")

SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
#(optional)SESSION_EXPIRE_AT_BROWSER_CLOSE = True 
CSRF_TRUSTED_ORIGINS = ['https://www.vahltech.com','https://vahltech.com','https://*.elasticbeanstalk.com']
SECURE_REDIRECT_EXEMPT = [r'^health/?$']


AWS_STORAGE_BUCKET_NAME = os.environ.get("AWS_STORAGE_BUCKET_NAME")
AWS_S3_REGION_NAME = os.environ.get("AWS_S3_REGION_NAME", "us-east-1")
AWS_S3_OBJECT_PARAMETERS = {
    'CacheControl': 'max-age=86400',
}

STORAGES = {
    "default": {
        "BACKEND": "storages.backends.s3boto3.S3Boto3Storage",
        "OPTIONS": {
            "bucket_name": AWS_STORAGE_BUCKET_NAME,
            "region_name": AWS_S3_REGION_NAME,
            "object_parameters": AWS_S3_OBJECT_PARAMETERS,
            "location": "media",
        },
    },
    "staticfiles": {
        "BACKEND": "storages.backends.s3boto3.S3StaticStorage",
        "OPTIONS": {
            "bucket_name": AWS_STORAGE_BUCKET_NAME,
            "region_name": AWS_S3_REGION_NAME,
            "object_parameters": AWS_S3_OBJECT_PARAMETERS,
            "location": "static",
        },
    },
}

AWS_STATIC_LOCATION = 'static'
AWS_S3_CUSTOM_DOMAIN = f"{AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com"
STATIC_URL = f'https://{AWS_S3_CUSTOM_DOMAIN}/{AWS_STATIC_LOCATION}/'
MEDIA_URL = f"https://{AWS_S3_CUSTOM_DOMAIN}/media/"

SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
USE_X_FORWARDED_HOST = True
SECURE_SSL_REDIRECT = True