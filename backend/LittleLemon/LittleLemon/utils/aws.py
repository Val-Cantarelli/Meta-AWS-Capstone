import os
import json
import boto3
from botocore.exceptions import ClientError

def get_db_credentials():
    """
    Fetches RDS credentials from AWS Secrets Manager.
    Expects the secret name in the DB_SECRET_NAME environment variable.
    """
    secret_name = os.environ["DB_SECRET_NAME"]
    region_name = boto3.session.Session().region_name or "us-east-1"

    try:
        client = boto3.client("secretsmanager", region_name=region_name)
        response = client.get_secret_value(SecretId=secret_name)
        secret = response["SecretString"]
        return json.loads(secret)  # returns dict with 'username' and 'password'
    except ClientError as e:
        raise RuntimeError(f"Failed to retrieve secret {secret_name}") from e
