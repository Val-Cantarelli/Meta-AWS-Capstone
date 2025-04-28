import os
from aws_cdk import (
    Stack,
    App,Duration,
    aws_lambda as _lambda,
)
from constructs import Construct

from lib.iam_roles.iam_roles import IamRoles


lambda_code_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../backend'))

class ComputeStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # IAM Role to Lambda
        lambda_role = IamRoles.create_lambda_execution_role(self)
        
        # Lambda Function
        self.lambda_function = _lambda.Function(
            self, "LittleLemonLambda",
            runtime=_lambda.Runtime.PYTHON_3_11,
            handler="lambda_function.handler", 
            code=_lambda.Code.from_asset(lambda_code_path), 
            memory_size=512,
            timeout=Duration.seconds(60),
            environment={
                "DJANGO_ENV": "production", 
            },
            role=lambda_role 
        )
        
app = App()
ComputeStack(app, "ComputeStack")
app.synth()