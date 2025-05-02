from .base import *
#from decouple import config

DEBUG = False
ALLOWED_HOSTS = [
    '9llvug30gg.execute-api.us-east-1.amazonaws.com'
]
'''DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': config('DB_NAME'),
        'USER': config('DB_USER'),
        'PASSWORD': config('DB_PASSWORD'),
        'HOST': config('DB_HOST'),
        'PORT': config('DB_PORT'),
        'OPTIONS': {
            'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
        },
    }
}
'''

#AWS_STORAGE_BUCKET_NAME = ('bucketname on aws')
#STATICFILES_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
#DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'

CSRF_COOKIE_SECURE = True
SESSION_COOKIE_SECURE = True
