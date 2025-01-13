# Meta AWS Capstone Project

This repository showcases my work in deploying a Django-based capstone project to AWS.  
The original project was developed as part of the [Meta Professional Certificate](https://www.coursera.org/professional-certificates/meta-back-end-developer), 
and this repository focuses on the **DevOps and cloud migration aspects**.

---

## Overview

The capstone project is a **restaurant website** built with Django. My work focused on:
1. Migrating the database to Amazon RDS.
2. Deploying the back-end to AWS Lambda using API Gateway.
3. Hosting static files (CSS, JS, images) in an S3 bucket, served through CloudFront.
4. Setting up CI/CD pipelines with AWS CodePipeline and CodeBuild.
5. Documenting the entire AWS infrastructure setup.

### Technologies and Services Used
- **Back-end Framework:** Django
- **Cloud Provider:** AWS
- **Services:**
  - **AWS Lambda:** Serverless hosting for the back-end.
  - **Amazon API Gateway:** API exposure for the Django app.
  - **Amazon RDS:** Relational database service for storing data.
  - **Amazon S3:** Storage for static and media files.
  - **Amazon CloudFront:** Content delivery network for faster static file loading.
  - **AWS CodePipeline & CodeBuild:** For CI/CD automation.

---
## Components

1. **Backend:** A Django REST API for managing a restaurant's operations.
   - Path: `/backend/`
   - Documentation: [Backend README](./backend/README.md)

2. **Frontend:** Static templates and assets for the restaurant's website.
   - Path: `/frontend/`
   - Documentation: [Frontend README](./frontend/README.md)

3. **DevOps:** AWS deployment and infrastructure as code.
   - Path: `/devops/`
   - Documentation: [DevOps README](./devops/README.md)


## Repository Structure

