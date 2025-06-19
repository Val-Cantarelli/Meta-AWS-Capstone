import os

from aws_cdk import (
    Stack,
    Duration,
    CfnOutput,
    aws_lambda as _lambda,
    aws_logs as logs,
    aws_iam as iam,
    aws_ec2 as ec2,
    aws_apigatewayv2 as apigw
)
from aws_cdk.aws_apigatewayv2 import CfnIntegration, CfnRoute, CfnStage
from aws_cdk.aws_lambda import Runtime
from constructs import Construct
from aws_cdk.aws_lambda_python_alpha import PythonFunction

from lib.iam_roles.iam_roles import IamRoles

lambda_code_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../backend'))

class ComputeStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)
        assert os.path.exists(os.path.join(lambda_code_path, "lambda_function.py")), "lambda_function.py not found"

        my_vpc = ec2.Vpc.from_lookup(self, "MyVPC", vpc_id="vpc-076af69e3bd55b0ee")

        private_subnet_1 = ec2.Subnet.from_subnet_id(self, "ComputeSubnet200", "subnet-00c55983c320de3b1")
        private_subnet_2 = ec2.Subnet.from_subnet_id(self, "ComputeSubnet201", "subnet-085c0350455dfef4f")

        lambda_role = IamRoles.create_lambda_execution_role(self)

        lambda_sg = ec2.SecurityGroup(
            self, "LambdaSG",
            vpc=my_vpc,
            description="SG for Lambda to access RDS Proxy",
            allow_all_outbound=True
        )        

        self.lambda_function = PythonFunction(
            self, "LittleLemonLambda",
            entry=lambda_code_path,
            runtime=Runtime.PYTHON_3_11,
            index="lambda_function.py",
            handler="lambda_handler",
            memory_size=512,
            timeout=Duration.seconds(180),
            environment={
                "DJANGO_ENV": "production",
                "DJANGO_SECRET_PARAM": "/littlelemon/django/SECRET_KEY",
                "DB_SECRET_NAME": "rds!db-4b54e2c7-9bee-42a5-b037-a9fd9218ffcb",
                "DB_NAME": "mysqlRDS_littlelemon",
                "DB_HOST": "proxydb2.proxy-cncggq6wib9a.us-east-1.rds.amazonaws.com",
                "DB_PORT": "3306",
            },
            role=lambda_role,
            vpc=my_vpc,
            vpc_subnets=ec2.SubnetSelection(subnets=[
                private_subnet_1,
                private_subnet_2
            ]),
            security_groups=[lambda_sg],
            bundling={
                "asset_excludes": [".env", ".env.*", "*.pyc", "__pycache__", "cdk.out", ".venv", "backup.sql"]
            }
        )

        http_api = apigw.CfnApi(
            self, "LittleLemonHttpApi",
            name="LittleLemonApi",
            protocol_type="HTTP"
        )

        lambda_integration = CfnIntegration(
            self, "LambdaIntegration",
            api_id=http_api.ref,
            integration_type="AWS_PROXY",
            integration_uri=self.lambda_function.function_arn,
            integration_method="POST",
            payload_format_version="2.0"
        )

        self.lambda_function.add_permission(
            "ApiInvokePermission",
            principal=iam.ServicePrincipal("apigateway.amazonaws.com"),
            action="lambda:InvokeFunction",
            source_arn=f"arn:aws:execute-api:{self.region}:{self.account}:{http_api.ref}/*/*/*"
        )
        

        CfnRoute(
            self, "RootRoute",
            api_id=http_api.ref,
            route_key="ANY /",
            target=f"integrations/{lambda_integration.ref}"
        )

        CfnRoute(
            self, "CatchAllRoute",
            api_id=http_api.ref,
            route_key="ANY /{proxy+}",
            target=f"integrations/{lambda_integration.ref}"
        )
        
        
        log_group = logs.LogGroup(self, "ApiLogs")
        log_group.grant_write(lambda_role)

        CfnStage(
            self, "ManualStage",
            api_id=http_api.ref,
            stage_name="v1",
            auto_deploy=True
        )

        CfnOutput(self, "ApiId", value=http_api.ref)
        CfnOutput(self, "ApiEndpoint", value=f"https://{http_api.ref}.execute-api.{self.region}.amazonaws.com/v1")
