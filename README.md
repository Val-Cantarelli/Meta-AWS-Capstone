# Meta AWS Capstone Project

This repository showcases my work in deploying a Django-based capstone project to AWS.  
The original project was developed as part of the [Meta Professional Certificate](https://www.coursera.org/professional-certificates/meta-back-end-developer), 
and this repository focuses on the DevOps and cloud migration aspects.


## Live
- https://www.vahltech.com


## Overview

The capstone project is a restaurant website built with Django. This repository focuses on:
1. Migrating the database to Amazon RDS.
2. Deploying the back-end to AWS Lambda + API Gateway.
3. Hosting static and media files in Amazon S3 (CloudFront is planned/optional).
4. Setting up CI/CD (evaluating GitHub Actions vs. AWS native tools).
5. Documenting the AWS infrastructure and operational setup.


## Architecture (current)

- Frontend: Django app on AWS Elastic Beanstalk (Python 3.12 AL2023, ASGI: Gunicorn + Uvicorn).
- API: AWS Lambda behind Amazon API Gateway.
- Database: Amazon RDS, accessed by Lambda via Amazon RDS Proxy.
- Assets: Amazon S3 for static/media. CDN (CloudFront) optional.

```mermaid
flowchart LR
  Client --> ALB[Application Load Balancer]
  ALB --> EB[Elastic Beanstalk (Django)]
  EB --> S3[(Amazon S3: static/media)]
  EB --> APIGW[API Gateway]
  APIGW --> L[Lambda]
  L --> RDSProxy[RDS Proxy] --> RDS[(Amazon RDS)]
```


## Technologies and Services Used
- Back-end Framework: Django + DRF (Django REST Framework)
- Authentication: JWT for API authentication/authorization
- Cloud Provider: AWS
- Services:
  - AWS Elastic Beanstalk (frontend hosting)
  - AWS Lambda (back-end compute)
  - Amazon API Gateway (API exposure)
  - Amazon RDS (database)
  - Amazon RDS Proxy (connection pooling for Lambda)
  - Amazon S3 (static/media)
  - Amazon CloudFront (CDN – optional/roadmap)
- CI/CD: evaluating GitHub Actions and/or AWS native tools


## Versions

### Version 1 (Current)
- Frontend on Elastic Beanstalk (ASGI: Gunicorn + Uvicorn).
- Backend on AWS Lambda + API Gateway.
- Lambda connects to RDS via RDS Proxy to minimize cold-start connection issues and improve pooling/security.
- Purpose: validate frontend integration and API functionality in the cloud with reliable DB connectivity.

### Version 2 (Planned)
- Backend migrated from Lambda to ECS Fargate.
- Purpose: support ASGI/WebSockets and future scalability with greater control over runtime and networking.

---

## Components

1. Backend
   - Django REST API for restaurant operations.
   - Path: `/backend/`
   - Link: (pending)

2. Frontend
   - Django UI/templates and static assets.
      - Path: `/frontend/`
      - Documentation: [`frontend/README.md`](./frontend/README.md)

3. DevOps / IaC
   - AWS deployment and infrastructure (experiments, CDK prototypes).
   - Path: `/littlelemon-backend-cdk/`
   - Documentation: [`littlelemon-backend-cdk/README.md`](./littlelemon-backend-cdk/README.md)



## Repository Structure
- `backend/` – Django REST API (Lambda-focused code and artifacts)
- `frontend/` – Django UI app (Elastic Beanstalk deployment)
- `littlelemon-backend-cdk/` – Infrastructure experiments (AWS CDK)
- `littlelemon-documentation/` – Architecture docs and diagrams

