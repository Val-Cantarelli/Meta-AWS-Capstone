#!/bin/bash
cd ../backend

# Load environment variables from file
export $(grep -v '^#' .env | xargs)

cd ../littlelemon-backend-cdk

# Run CDK deploy
echo "Running CDK deploy..."
cdk deploy