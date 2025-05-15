# iam_roles.py
from aws_cdk import aws_iam as iam
from aws_cdk import Stack  


class IamRoles:
    
    @staticmethod
    def create_lambda_execution_role(scope: Stack) -> iam.Role:
        lambda_role = iam.Role(
            scope, "LambdaExecutionRole",
            assumed_by=iam.ServicePrincipal("lambda.amazonaws.com"),
        )

        lambda_role.add_managed_policy(
            iam.ManagedPolicy.from_aws_managed_policy_name("service-role/AWSLambdaBasicExecutionRole")
        )
        lambda_role.add_managed_policy(
            iam.ManagedPolicy.from_aws_managed_policy_name("AmazonRDSFullAccess")
        )
        # SSM to secret_key Django
        lambda_role.add_to_policy(
            iam.PolicyStatement(
            actions=["ssm:GetParameter"],
            resources=["arn:aws:ssm:us-east-1:557690602441:parameter/littlelemon/django/SECRET_KEY"]
            )
        )
        # Secret Manager to db credential
        lambda_role.add_to_policy(
            iam.PolicyStatement(
                actions=["secretsmanager:GetSecretValue"],
                resources=["arn:aws:secretsmanager:us-east-1:557690602441:secret:credentialsRDSprod-*"]
            )
        )
        # 
        lambda_role.add_to_policy(
            iam.PolicyStatement(
                actions=[
                "ec2:CreateNetworkInterface",
                "ec2:DescribeNetworkInterfaces",
                "ec2:DeleteNetworkInterface"
            ],
            resources=["*"]  
            )
        )

        return lambda_role
    
    
    @staticmethod
    def create_rds_proxy_role(scope: Stack) -> iam.Role:
        proxy_role=iam.Role(
            scope,"RDSProxyRole",
            assumed_by=iam.ServicePrincipal("rds.amazonaws.com"),
            description="Custom Role for RDS Proxy Access",
        )
        
        proxy_role.add_to_policy(
            iam.PolicyStatement(
                actions=[
                    "secretsmanager:GetSecretValue",
                    "secretsmanager:DescribeSecret",
                    "secretsmanager:ListSecrets",
                    "rds-db:connect"
                ],
                resources=[
                    "arn:aws:secretsmanager:us-east-1:557690602441:secret:credentialsRDSprod-icEXUK",
                    "arn:aws:rds:us-east-1:557690602441:db:database-1"
                ]
            )
        )
        
        return proxy_role
    
    
    
    
