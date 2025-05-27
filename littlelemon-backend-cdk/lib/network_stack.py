from aws_cdk import Stack, CfnTag,CfnOutput
from aws_cdk import aws_ec2 as ec2
from constructs import Construct

class NetworkStack(Stack):
    def __init__(self, scope: Construct, construct_id: str, **kwargs):
        super().__init__(scope, construct_id, **kwargs)

        # VPC Lookup
        my_vpc = ec2.Vpc.from_lookup(self, "MyExistingVPC", vpc_id="vpc-076af69e3bd55b0ee")

        # Creates the private subnets
        private_subnet_1 = ec2.CfnSubnet(
            self, "PrivateSubnet1",
            vpc_id=my_vpc.vpc_id,
            cidr_block="172.31.200.0/24",
            availability_zone="us-east-1a",
            map_public_ip_on_launch=False,
            tags=[
                CfnTag(key="aws-cdk:subnet-type", value="Isolated"),
                CfnTag(key="aws-cdk:subnet-name", value="PrivateSubnet200")
            ]
        )
        
        private_subnet_2 = ec2.CfnSubnet(
            self, "PrivateSubnet2",
            vpc_id=my_vpc.vpc_id,
            cidr_block="172.31.201.0/24",
            availability_zone="us-east-1b",
            map_public_ip_on_launch=False,
            tags=[
                CfnTag(key="aws-cdk:subnet-type", value="Isolated"),
                CfnTag(key="aws-cdk:subnet-name", value="PrivateSubnet201")
            ]
        )
    
        # Creates a private Route Table
        private_route_table = ec2.CfnRouteTable(
            self, "PrivateRouteTable",
            vpc_id=my_vpc.vpc_id
        )
        
        # Associate the subnets to the private Route Table
        ec2.CfnSubnetRouteTableAssociation(
            self, "PrivateSubnet1Association",
            subnet_id=private_subnet_1.ref,
            route_table_id=private_route_table.ref
        )

        ec2.CfnSubnetRouteTableAssociation(
            self, "PrivateSubnet2Association",
            subnet_id=private_subnet_2.ref,
            route_table_id=private_route_table.ref
        )

        subnet1_ref = ec2.Subnet.from_subnet_id(self, "SubnetRef1", private_subnet_1.ref)
        subnet2_ref = ec2.Subnet.from_subnet_id(self, "SubnetRef2", private_subnet_2.ref)

        # VPC Endpoint for SSM
        ssm_endpoint = ec2.InterfaceVpcEndpoint(self, "SSMEndpoint",
            vpc=my_vpc,
            service=ec2.InterfaceVpcEndpointService("com.amazonaws.us-east-1.ssm"),
            subnets=ec2.SubnetSelection(subnets=[subnet1_ref, subnet2_ref])
        )

        # VPC Endpoint for Secrets Manager
        secrets_manager_endpoint = ec2.InterfaceVpcEndpoint(self, "SecretsManagerEndpoint",
            vpc=my_vpc,
            private_dns_enabled=True,
            service=ec2.InterfaceVpcEndpointService("com.amazonaws.us-east-1.secretsmanager"),
            subnets=ec2.SubnetSelection(subnets=[subnet1_ref, subnet2_ref])
        )

        # Optionally, export endpoint URLs for debugging purposes
        CfnOutput(self, "SSMEndpointId", value=ssm_endpoint.vpc_endpoint_id,export_name="SSMVPCEndpointId")
        CfnOutput(self, "SecretsManagerEndpointId", value=secrets_manager_endpoint.vpc_endpoint_id,export_name="SecretsManagerVPCEndpointId")