import os
from aws_cdk import (
    Stack,
    App,
    Duration,
    aws_lambda as _lambda,
    aws_iam as iam,
    aws_apigatewayv2 as apigwv2,
    aws_apigatewayv2_integrations as integrations,
    CfnOutput, 
)
from aws_cdk.aws_lambda_python_alpha import PythonFunction
from aws_cdk.aws_lambda import Runtime
from constructs import Construct

from lib.iam_roles.iam_roles import IamRoles

# path to lambda_function ans requirements.txt
lambda_code_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../backend'))

class ComputeStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)
        assert os.path.exists(os.path.join(lambda_code_path, "lambda_function.py")), "lambda_function.py não encontrado"


        # IAM Role to Lambda
        lambda_role = IamRoles.create_lambda_execution_role(self)
        
        # Lambda Function
        self.lambda_function = PythonFunction(
            self, "LittleLemonLambda",
            entry=lambda_code_path,
            runtime=Runtime.PYTHON_3_11,
            index="lambda_function.py", 
            handler="handler", 
            memory_size=512,
            timeout=Duration.seconds(60),
            environment={
                "DJANGO_ENV": "production",
                "DJANGO_SECRET_PARAM": "/littlelemon/django/SECRET_KEY",
                "DB_SECRET_NAME": "credentialsRDSprod",
                "DB_NAME": "mysqlRDS_littlelemon",
                "DB_HOST": "database-1.cncggq6wib9a.us-east-1.rds.amazonaws.com",
                "DB_PORT": "3306",
            },
            role=lambda_role,
            bundling={
                "asset_excludes": [".env", ".env.*", "*.pyc", "__pycache__", "cdk.out", ".venv", "backup.sql"]
            }
        )
        
        # API Gateway HTTP - integration
        lambda_integration = integrations.HttpLambdaIntegration(
            "LittleLemonLambdaIntegration", self.lambda_function
        )

        api_gateway = apigwv2.HttpApi(
            self, "LittleLemonHttpApi",
            default_integration=lambda_integration
        )

        CfnOutput(self, "APIEndpoint", value=api_gateway.url)
        
app = App()
ComputeStack(app, "ComputeStack")
app.synth()