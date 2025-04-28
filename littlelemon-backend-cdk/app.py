#!/usr/bin/env python3
import os

from aws_cdk import App  
from lib.compute_stack import ComputeStack 

app = App()

# Instanciates the ComputeStack
ComputeStack(app, "ComputeStack")

# Generates the CloudFormation's template
app.synth()
