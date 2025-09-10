import os
import boto3
import json
import logging
import django
import importlib
import sys
import traceback
from mangum import Mangum
from pythonjsonlogger import jsonlogger

# ------------------------
# Logger JSON configurado
# ------------------------
class LambdaJsonFormatter(jsonlogger.JsonFormatter):
    def process_log_record(self, log_record):
        exc_info = log_record.pop("exc_info", None)
        if exc_info:
            ex_type = exc_info[0].__name__ if exc_info[0] else None
            ex_msg = str(exc_info[1]) if exc_info[1] else None
            log_record["exception_type"] = ex_type
            log_record["exception_message"] = ex_msg
            log_record["stacktrace"] = "".join(traceback.format_exception(*exc_info))
        return super().process_log_record(log_record)


logger = logging.getLogger()
logger.setLevel(logging.INFO)
logger.handlers = []

handler = logging.StreamHandler(sys.stdout)
formatter = LambdaJsonFormatter(
    '%(asctime)s %(levelname)s %(name)s %(message)s'
)
handler.setFormatter(formatter)
logger.addHandler(handler)

# ------------------------
# Config Django
# ------------------------
ENV = os.getenv("DJANGO_ENV", "production")
os.environ.setdefault("DJANGO_SETTINGS_MODULE", f"LittleLemon.LittleLemon.settings.{ENV}")

logger.info(f"Starting application with environment: {ENV}")

try:
    settings_module = f"LittleLemon.LittleLemon.settings.{ENV}"
    importlib.import_module(settings_module)
    logger.info(f"Settings module {settings_module} loaded successfully.")
except Exception:
    logger.exception(f"Failed to import settings module: {settings_module}")

# Keep it this import here!!
from LittleLemon.LittleLemon.asgi import application
django.setup()

# ------------------------
# Lambda handler
# ------------------------
def lambda_handler(event, context):
    # injeta aws_request_id no log
    extra = {"aws_request_id": getattr(context, "aws_request_id", None)}
    logger.info("Lambda invoked", extra=extra)
    
    mangum_handler = Mangum(application, lifespan="off", api_gateway_base_path="/v1")
    return mangum_handler(event, context)

# ------------------------
# Secret Manager helper
# ------------------------
def get_db_credentials(secret_name: str, region_name="us-east-1"):
    client = boto3.client('secretsmanager', region_name=region_name)
    try:
        logger.info(f"Fetching secret: {secret_name}")
        get_secret_value_response = client.get_secret_value(SecretId=secret_name)
        if 'SecretString' in get_secret_value_response:
            secret = json.loads(get_secret_value_response['SecretString'])
            logger.info(f"Secret fetched successfully: {secret_name}")
        else:
            logger.warning("SecretBinary found, but it's not supported in this case.")
            secret = json.loads(get_secret_value_response['SecretBinary'])
        return secret
    except Exception:
        logger.exception(f"Error accessing secret: {secret_name}")
        raise

# ------------------------
# Setup DB credentials
# ------------------------
try:
    db_secret = get_db_credentials(secret_name=os.environ['DB_SECRET_NAME'])
    os.environ["DB_USER"] = db_secret["username"]
    os.environ["DB_PASSWORD"] = db_secret["password"]
    logger.info("Database credentials set successfully.")
except Exception:
    logger.exception("Failed to set DB credentials")
    raise
