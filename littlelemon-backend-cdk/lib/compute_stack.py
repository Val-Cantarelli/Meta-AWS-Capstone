import os

from aws_cdk import (
    Stack,
    App,
    Duration,
    Fn,
    aws_lambda as _lambda,
    aws_iam as iam,
    CfnOutput, 
    aws_ec2 as ec2
)
from aws_cdk.aws_apigatewayv2 import HttpApi, CfnApi
from aws_cdk.aws_apigatewayv2_integrations import HttpLambdaIntegration
from aws_cdk.aws_lambda import Runtime
from constructs import Construct
from aws_cdk.aws_lambda_python_alpha  import PythonFunction

from lib.iam_roles.iam_roles import IamRoles


# path to lambda_function ans requirements.txt
lambda_code_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../backend'))

class ComputeStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)
        assert os.path.exists(os.path.join(lambda_code_path, "lambda_function.py")), "lambda_function.py not found"
        
        # VPC Lookup
        my_vpc = ec2.Vpc.from_lookup(self, "MyVPC", vpc_id="vpc-076af69e3bd55b0ee")

        # Private subnets
        private_subnet_1 = ec2.Subnet.from_subnet_id(self, "ComputeSubnet200", "subnet-00c55983c320de3b1")
        private_subnet_2 = ec2.Subnet.from_subnet_id(self, "ComputeSubnet201", "subnet-085c0350455dfef4f")
        
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
        lambda_sg.add_egress_rule(
            peer=ec2.Peer.security_group_id(proxy_sg.security_group_id),
            connection=ec2.Port.tcp(3306),
            description="Allow Lambda access RDS Proxy"
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
                "RDS_PROXY_ENDPOINT": Fn.import_value("RdsProxyEndpoint"),
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
        
        
        
        # API Gateway HTTP - integration
        lambda_integration = HttpLambdaIntegration("LambdaIntegration", self.lambda_function)
        
        vpc_endpoint_id = "vpce-0bb9c7fd4b4270bb9"
        
        
        http_api = HttpApi(
            self, "LittleLemonHttpApi",
            default_integration=lambda_integration,
            disable_execute_api_endpoint=True,
            create_default_stage=True,    
            api_name="LittleLemonApi")
        
        
        li_api = http_api.node.default_child
        li_api.policy = {
            "Version": "2012-10-17",
            "Statement": [{
                "Effect": "Allow",
                "Principal": "*",
                "Action": "execute-api:Invoke",
                "Resource": "*",
                "Condition": {
                    "StringEquals": {
                     "aws:SourceVpce": "vpce-0bb9c7fd4b4270bb9"
                     }
                }
            }]
        }

        # Output the API ID and other useful information
        CfnOutput(self, "ApiId", value=http_api.api_id)
        CfnOutput(self, "ApiEndpoint", value=http_api.url or "")

