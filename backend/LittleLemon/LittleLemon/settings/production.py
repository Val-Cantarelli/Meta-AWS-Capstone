from .base import *

DEBUG = False
ALLOWED_HOSTS = ['*']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'mysqlRDS_littlelemon',
        'USER': 'admin',
        'PASSWORD': 'aIj5se6Pijrj22iqJEua',
        'HOST': 'database-1.cncggq6wib9a.us-east-1.rds.amazonaws.com',
        'PORT': '3306',
        'OPTIONS': {
            'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
        },
    }
}

AWS_STORAGE_BUCKET_NAME = 'zappa-ql19nrdtr'
STATICFILES_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'

CSRF_COOKIE_SECURE = True
SESSION_COOKIE_SECURE = True
