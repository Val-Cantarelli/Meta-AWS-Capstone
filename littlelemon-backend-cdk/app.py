#!/usr/bin/env python3
import os
from aws_cdk import App, Environment
from lib.compute_stack import ComputeStack
from lib.network_stack import NetworkStack
from lib.database_stack import DatabaseStack


PROFILE_NAME = "mfa-profile"

account = os.popen(f'aws sts get-caller-identity --query "Account" --output text --profile {PROFILE_NAME}').read().strip()
region = os.popen(f'aws configure get region --profile {PROFILE_NAME}').read().strip()

if not account or not region:
    raise RuntimeError("Fail: verify AWS credentials")

env = Environment(account=account, region=region)

app = App()

ComputeStack(app, "ComputeStack", env=env)
NetworkStack(app, "NetworkStack", env=env)
DatabaseStack(app, "DatabaseStack", env=env)
app.synth()
