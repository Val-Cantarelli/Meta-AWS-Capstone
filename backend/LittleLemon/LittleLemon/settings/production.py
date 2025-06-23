from .base import *
import os
import boto3
from ..utils.aws import get_db_credentials

DEBUG = False
ALLOWED_HOSTS = [
    '6qpkzrhv4c.execute-api.us-east-1.amazonaws.com'
]

def get_parameter(param_name: str) -> str:
    ssm = boto3.client("ssm", region_name=os.environ.get("AWS_REGION", "us-east-1"))
    response = ssm.get_parameter(Name=param_name, WithDecryption=True)
    return response["Parameter"]["Value"]

SECRET_KEY = get_parameter(os.environ["DJANGO_SECRET_PARAM"])
if not SECRET_KEY:
    raise RuntimeError("SECRET_KEY not fetched from SSM")

secrets = get_db_credentials()

rds_proxy_endpoint = os.environ.get("DB_HOST")
if not rds_proxy_endpoint:
    raise RuntimeError("DB_HOST not set in environment variables")

'''
Na paginacao sobrescrever o get_next_link e get_previous_link para que a URL seja /v1/api/ em vez de /api/
from rest_framework.pagination import PageNumberPagination

class APIGatewayPageNumberPagination(PageNumberPagination):
    def get_next_link(self):
        url = super().get_next_link()
        if url:
            return url.replace('/api/', '/v1/api/', 1)
        return url

    def get_previous_link(self):
        url = super().get_previous_link()
        if url:
            return url.replace('/api/', '/v1/api/', 1)
        return url
        
        
REST_FRAMEWORK = {
    "DEFAULT_PAGINATION_CLASS": "LittleLemon.settings.production.APIGatewayPageNumberPagination",
}
    
'''


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': os.environ["DB_NAME"],
        'USER': secrets["username"],
        'PASSWORD': secrets["password"],
        'HOST': rds_proxy_endpoint,
        'PORT': os.environ.get("DB_PORT", "3306"),
        'OPTIONS': {
            'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
        },
    }
}
required_env_vars = ["DB_NAME","DB_HOST", "DB_SECRET_NAME", "DJANGO_SECRET_PARAM"]
for var in required_env_vars:
    if not os.environ.get(var):
        raise RuntimeError(f"Missing required environment variable: {var}")


#AWS_STORAGE_BUCKET_NAME = ('bucketname on aws')
#STATICFILES_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
#DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'

CSRF_COOKIE_SECURE = True
SESSION_COOKIE_SECURE = True
