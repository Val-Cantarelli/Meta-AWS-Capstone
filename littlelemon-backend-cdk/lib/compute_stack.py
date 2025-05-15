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
    aws_ec2 as ec2
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
        
        # VPC Lookup
        my_vpc = ec2.Vpc.from_lookup(self, "MyVPC", vpc_id="vpc-076af69e3bd55b0ee")

        # IAM Role to Lambda
        lambda_role = IamRoles.create_lambda_execution_role(self)
        
        # SG Lambda
        lambda_sg = ec2.SecurityGroup(
            self, "LambdaSG",
            vpc=my_vpc,
            description="SG for Lambda to access RDS Proxy",
            allow_all_outbound=True  
        )     
        
        # Lambda access RDS Proxy SG
        proxy_sg = ec2.SecurityGroup.from_security_group_id(self, "ProxySG", "sg-037c88deadba79c4d")

        proxy_sg.add_ingress_rule(
            peer=lambda_sg,
            connection=ec2.Port.tcp(3306),
            description="Allow Lambda to access RDS Proxy"
        )        
           
        # Lambda Function
        self.lambda_function = PythonFunction(
            self, "LittleLemonLambda",
            entry=lambda_code_path,
            runtime=Runtime.PYTHON_3_11,
            index="lambda_function.py", 
            handler="handler", 
            memory_size=512,
            timeout=Duration.seconds(180),
            environment={
                "DJANGO_ENV": "production",
                "DJANGO_SECRET_PARAM": "/littlelemon/django/SECRET_KEY",
                "DB_SECRET_NAME": "credentialsRDSprod",
                "DB_NAME": "mysqlRDS_littlelemon",
                "DB_HOST": "database-1.cncggq6wib9a.us-east-1.rds.amazonaws.com",
                "DB_PORT": "3306",
            },
            role=lambda_role,
            vpc=my_vpc,
            vpc_subnets=ec2.SubnetSelection(subnets=[
                ec2.Subnet.from_subnet_id(self, "PrivateSubnet200", "subnet-00c55983c320de3b1"),
                ec2.Subnet.from_subnet_id(self, "PrivateSubnet201", "subnet-085c0350455dfef4f")
            ]),
            security_groups=[lambda_sg],
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
        
