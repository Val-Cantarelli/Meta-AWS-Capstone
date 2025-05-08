# iam_roles.py
from aws_cdk import aws_iam as iam
from aws_cdk import Stack  # Usando App e Stack do CDK v2

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

        return lambda_role
