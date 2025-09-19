from diagrams import Diagram, Cluster
from diagrams.aws.compute import LambdaFunction, EC2
from diagrams.aws.database import RDS
from diagrams.aws.network import APIGateway
from diagrams.aws.storage import S3

with Diagram("AWS Architecture - Little Lemon Project", show=True, direction="TB"):

    with Cluster("AWS Cloud"):
        api_gateway = APIGateway("HTTP API Gateway")
        s3 = S3("S3 Static Files")
        beanstalk = EC2("Elastic Beanstalk Frontend")

        with Cluster("VPC"):
            with Cluster("Private Subnets"):
                lambda_fn = LambdaFunction("Django API Lambda")
                rds_proxy = RDS("RDS Proxy")
                rds = RDS("MySQL RDS")
                lambda_fn >> rds_proxy >> rds

            openvpn = EC2("OpenVPN Server")

        api_gateway >> lambda_fn
        beanstalk >> api_gateway
        beanstalk >> s3
        openvpn >> lambda_fn
