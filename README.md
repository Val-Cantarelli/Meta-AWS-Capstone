# Meta AWS Capstone Project

This repository showcases my work in deploying a Django-based capstone project to AWS.  
The original project was developed as part of the [Meta Professional Certificate](https://www.coursera.org/professional-certificates/meta-back-end-developer), 
and this repository focuses on the **DevOps and cloud migration aspects**.


## Overview

The capstone project is a **restaurant website** built with Django. My work focused on:
1. Migrating the database to Amazon RDS.
2. Deploying the back-end to AWS Lambda + API Gateway.
3. Hosting static files (CSS, JS, images) in an S3 bucket, served through CloudFront.
4. Setting up CI/CD pipelines with AWS CodePipeline and CodeBuild.
5. Documenting the entire AWS infrastructure setup.

### Technologies and Services Used
- **Back-end Framework:** Django + DRF (Django Rest Framework)
- **Authentication:** JWT (JSON Web Tokens) for secure API authentication and authorization.
- **Cloud Provider:** AWS
- **Services:**
   - **AWS Lambda:** Serverless hosting for the back-end.
   - **Amazon API Gateway:** API exposure for the Django app.
   - **Amazon RDS:** Relational database service for storing data.
   - **Amazon RDS Proxy:** Connection pooling and improved database performance for Lambda functions. (Planned feature, currently under evaluation)
   - **Amazon S3:** Storage for static and media files.
   - **Amazon CloudFront:** Content delivery network for faster static file loading.
- **CI/CD pipeline:** * currently evaluating between AWS native tools and GitHub Actions for automation.*


## Components

1. **Backend:** 
   - A Django REST API for managing a restaurant's operations.
   - Link: (pending)

2. **Frontend:** 
   - Static templates and assets for the restaurant's website.
   - Link: (pending)

3. **DevOps(littlelemon-backend-cdk):** 
   - AWS deployment and infrastructure as code.
   - Link: (pending)

4. **Documentation(littlelemon-documentation):** Comprehensive technical and business documentation detailing the AWS infrastructure, deployment processes, and operational best practices.


## Running Locally

1. Clone the repository.
2. Create a virtual environment and install dependencies:
python -m .venv source .venv/bin/activate pip install -r requirements.txt
3. Configure environment variables in `.env`.
4. Run migrations: python manage,py migrate
5. Start the development server: python manage.py runserver

## Django Admin

- Link to doc: (pending)

## Contributing

Pull requests are welcome! For major changes, please open an issue first to discuss what you would like to change.

## Author

- [Valdielen Casarin](https://www.linkedin.com/in/valdielen-casarin/)