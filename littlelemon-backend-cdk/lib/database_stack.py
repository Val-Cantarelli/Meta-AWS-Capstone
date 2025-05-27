from aws_cdk import (
    Stack,
    aws_rds as rds,
    aws_ec2 as ec2,
    aws_secretsmanager as secretsmanager,
    aws_iam as iam,
    Duration,
    CfnOutput 
)
from constructs import Construct
from lib.iam_roles.iam_roles import IamRoles

class DatabaseStack(Stack):
    def __init__(self, scope: Construct, construct_id: str, **kwargs):
        super().__init__(scope, construct_id, **kwargs)

        my_vpc = ec2.Vpc.from_lookup(self, "MyVPC", vpc_id="vpc-076af69e3bd55b0ee")
        
        
        private_subnet_1 = ec2.Subnet.from_subnet_id(self, "DatabaseSubnet200", "subnet-00c55983c320de3b1")
        private_subnet_2 = ec2.Subnet.from_subnet_id(self, "DatabaseSubnet201", "subnet-085c0350455dfef4f")


        db_secret = secretsmanager.Secret.from_secret_name_v2(
            self, "DBSecret", "credentialsRDSprod"
        )

        db_instance = rds.DatabaseInstance.from_database_instance_attributes(
            self, "RDSInstance",
            instance_endpoint_address="database-1.cncggq6wib9a.us-east-1.rds.amazonaws.com",
            instance_identifier="database-1",
            port=3306,
            engine=rds.DatabaseInstanceEngine.mysql(version=rds.MysqlEngineVersion.VER_8_0),
            security_groups=[
                ec2.SecurityGroup.from_security_group_id(self, "SG1", "sg-037c88deadba79c4d"),
                ec2.SecurityGroup.from_security_group_id(self, "SG2", "sg-040aebaff168e3f85")
            ]
        )
    
        proxy_role = IamRoles.create_rds_proxy_role(self)
        # RDS Proxy
        self.rds_proxy = rds.DatabaseProxy(
            self, "LittleLemonRDSProxy",
            proxy_target=rds.ProxyTarget.from_instance(db_instance),
            secrets=[db_secret],
            vpc=my_vpc,
            role=proxy_role,
            require_tls=True,
            iam_auth=False,
            vpc_subnets=ec2.SubnetSelection(subnets=[private_subnet_1, private_subnet_2]),
            security_groups=[
                ec2.SecurityGroup.from_security_group_id(self, "ProxySG", "sg-037c88deadba79c4d")
            ],
            max_connections_percent=100,
            idle_client_timeout=Duration.seconds(300)
        )
        # Export endpoint RDS Proxy
        CfnOutput(self, "RdsProxyEndpoint",
                       value=self.rds_proxy.endpoint,
                       description="RDS Proxy Endpoint"
        )
        
        
