import os
import boto3
import json
import logging

import django
from mangum import Mangum

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()

ENV = os.getenv("DJANGO_ENV", "production")
os.environ.setdefault("DJANGO_SETTINGS_MODULE", f"LittleLemon.LittleLemon.settings.{ENV}")

logger.info(f"Starting application with environment: {ENV}")

import importlib
try:
    settings_module = f"LittleLemon.LittleLemon.settings.{ENV}"
    importlib.import_module(settings_module)
    logger.info(f"Settings module {settings_module} loaded successfully.")
except Exception as e:
    logger.error(f"Failed to import settings module: {settings_module}\n{e}")

# Keep it this import here!!
from LittleLemon.LittleLemon.asgi import application
django.setup()

handler = Mangum(application, lifespan="off")

#test
def lambda_handler(event, context):
    print(json.dumps(event)) 
    return handler(event, context)

# Access to Secret Manager
def get_db_credentials(secret_name: str, region_name="us-east-1"):
    # Creating the client of Secret Manager
    client = boto3.client('secretsmanager', region_name=region_name)
    
    try:
        logger.info(f"Fetching secret: {secret_name}")
        get_secret_value_response = client.get_secret_value(SecretId=secret_name)
        
        # Process the secret
        if 'SecretString' in get_secret_value_response:
            secret = json.loads(get_secret_value_response['SecretString'])
            logger.info(f"Secret fetched successfully: {secret_name}")
        else:
            logger.warning("SecretBinary found, but it's not supported in this case.")
            secret = json.loads(get_secret_value_response['SecretBinary'])

        return secret

    except Exception as e:
        logger.error(f"Error to access the secret: {e}")
        raise e

# Credentials DB
try:
    db_secret = get_db_credentials(secret_name=os.environ['DB_SECRET_NAME'])
    
    # Set environment variables for DB credentials
    os.environ["DB_USER"] = db_secret["username"]
    os.environ["DB_PASSWORD"] = db_secret["password"]
    os.environ["DB_HOST"] = db_secret["host"]
    os.environ["DB_PORT"] = db_secret["port"]
    
    logger.info("Database credentials set successfully.")
except Exception as e:
    logger.error(f"Failed to set DB credentials: {e}")
    raise e
