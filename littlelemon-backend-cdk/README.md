
# Little Lemon Backend Infrastructure (CDK)

AWS CDK Infrastructure as Code for the Little Lemon API backend, implementing a serverless architecture with Lambda functions, API Gateway, and RDS database with VPC networking.

## Architecture Overview

This CDK project deploys the backend infrastructure for the Little Lemon restaurant API:

- **Compute**: AWS Lambda function running Django REST API
- **API Gateway**: HTTP API for routing requests to Lambda
- **Database**: MySQL RDS instance with RDS Proxy for connection pooling
- **Networking**: VPC with private subnets and VPC endpoints
- **Security**: IAM roles, security groups, and Secrets Manager integration

## Project Structure

```
littlelemon-backend-cdk/
├── app.py                  # CDK application entry point
├── cdk.json               # CDK configuration
├── lib/                   # CDK stack definitions
│   ├── compute_stack.py   # Lambda & API Gateway resources
│   ├── network_stack.py   # VPC, subnets, and VPC endpoints  
│   ├── database_stack.py  # RDS instance and security groups
│   └── iam_roles/         # IAM role definitions
├── tests/                 # CDK unit tests
└── requirements-dev.txt   # Development dependencies
```

## Infrastructure Components

### Network Stack
- **VPC Lookup**: References existing VPC (`vpc-076af69e3bd55b0ee`)
- **Private Subnets**: Two isolated subnets across AZs for Lambda and RDS
- **VPC Endpoints**: SSM and Secrets Manager endpoints for secure access
- **Route Tables**: Private routing for isolated network traffic

### Compute Stack  
- **Lambda Function**: Python 3.11 runtime running Django API
- **API Gateway**: HTTP API with catch-all routing (`ANY /` and `ANY /{proxy+}`)
- **Security Groups**: Lambda security group for RDS access
- **Environment Variables**: Database connection and Django configuration
- **Memory/Timeout**: 512MB memory, 180-second timeout

### Database Stack
- **RDS Instance**: MySQL 8.0 database instance
- **RDS Proxy**: Connection pooling for Lambda connections
- **Secrets Manager**: Database credentials management
- **Security Groups**: Database access controls

## Prerequisites

1. **AWS Profile**: Configure AWS profile named `mfa-profile`
2. **Python Environment**: Python 3.8+ with CDK installed
3. **Node.js**: Required for CDK CLI
4. **Existing Resources**: VPC, RDS instance, and secrets must exist

## Setup and Deployment

### 1. Environment Setup
```bash
# Create virtual environment
python3 -m venv .venv
source .venv/bin/activate  # Linux/macOS
# .venv\Scripts\activate.bat  # Windows

# Install dependencies  
pip install -r requirements-dev.txt
npm install -g aws-cdk
```

### 2. AWS Configuration
```bash
# Configure AWS profile with MFA
aws configure --profile mfa-profile
aws sts get-caller-identity --profile mfa-profile
```

### 3. CDK Operations
```bash
# List all stacks
cdk ls

# Synthesize CloudFormation templates
cdk synth

# Deploy all stacks (requires existing resources)
cdk deploy --all --profile mfa-profile

# Deploy specific stack
cdk deploy NetworkStack --profile mfa-profile

# Compare with deployed state
cdk diff --profile mfa-profile

# Destroy infrastructure
cdk destroy --all --profile mfa-profile
```

## Configuration

### Environment Variables (Lambda)
- `DJANGO_ENV=production`
- `DJANGO_SECRET_PARAM`: SSM parameter for Django secret key
- `DB_SECRET_NAME`: Secrets Manager secret for database credentials
- `DB_NAME`: Database name (`mysqlRDS_littlelemon`)
- `DB_HOST`: RDS Proxy endpoint
- `DB_PORT`: Database port (3306)

### Resource Dependencies
The stacks reference existing AWS resources that must be configured:
- **VPC ID**: Configure in `app.py` and stack files
- **Subnets**: Private subnet IDs for Lambda deployment
- **RDS Instance**: Database endpoint for application connection
- **DB Secret**: Secrets Manager secret name for database credentials

**⚠️ Note**: Resource IDs and endpoints shown here are environment-specific. 
((For multi-environment deployment, consider externalizing these values to Parameter Store or CDK context.)

## Security Features

- **Private Networking**: Lambda runs in private subnets
- **VPC Endpoints**: No internet routing for AWS service access
- **IAM Roles**: Least-privilege access for Lambda execution
- **Secrets Management**: Database credentials stored in Secrets Manager
- **Security Groups**: Network-level access controls

## Outputs

After deployment, the stacks provide:
- **API Endpoint**: `https://{api-id}.execute-api.{region}.amazonaws.com/v1`
- **API ID**: For integration with frontend applications
- **VPC Endpoint IDs**: For debugging network connectivity

## Lambda Function Details

The Lambda function:
- **Runtime**: Python 3.11
- **Handler**: `lambda_function.lambda_handler`
- **Source**: Built from `../backend` directory
- **Bundling**: Excludes `.env`, `.venv`, and cache files
- **Memory**: 512MB for Django application needs
- **Timeout**: 180 seconds for complex API operations

## Development Workflow

1. **Local Development**: Test backend API locally before deployment
2. **Infrastructure Changes**: Modify CDK stacks in `lib/` directory
3. **Validation**: Use `cdk synth` to validate CloudFormation templates
4. **Deployment**: Deploy with `cdk deploy` after testing
5. **Monitoring**: Use CloudWatch logs for Lambda function monitoring

## Troubleshooting

### Common Issues
- **Credentials**: Verify `mfa-profile` AWS configuration
- **Dependencies**: Ensure all existing resources are available
- **Permissions**: Check IAM permissions for CDK deployment
- **VPC Configuration**: Validate subnet and security group settings

### Useful Commands
```bash
# Check CDK version
cdk --version

# Validate templates
cdk synth --quiet

# Check deployment diff
cdk diff NetworkStack

# View stack outputs
aws cloudformation describe-stacks --stack-name ComputeStack --profile mfa-profile
```

## Security Considerations

- **Database Access**: Lambda connects via private subnets only
- **API Security**: Implement authentication at application level
- **Secrets Rotation**: Consider implementing automatic secret rotation
- **VPC Flow Logs**: Enable for network traffic monitoring
- **CloudTrail**: Monitor API calls and infrastructure changes

## Project Credits

**Infrastructure Design**: Custom AWS CDK implementation for Little Lemon API
**Base Template**: AWS CDK Python project template
**Custom Components**: VPC networking, Lambda packaging, API Gateway integration
