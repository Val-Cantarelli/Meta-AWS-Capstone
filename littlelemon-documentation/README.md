# Little Lemon Restaurant API Documentation

> Meta AWS Capstone Project - Complete restaurant management system with Django REST API and AWS infrastructure.

## Documentation Index

### API Documentation
- **[Endpoints](./api/endpoints.md)** - Complete documentation of all endpoints
- **[Authentication](./api/authentication.md)** - JWT, tokens and authentication
- **[Permissions](./api/permissions.md)** - Access rules and user groups
- **[Examples](./api/examples.md)** - Practical examples of requests and responses

### Architecture
- **[AWS Infrastructure](./architecture/aws-infrastructure.md)** - AWS architecture and components
- **[Database Schema](./architecture/database-schema.md)** - Models and relationships
- **[Deployment](./architecture/deployment.md)** - Deployment process and CI/CD

### Development
- **[Setup Guide](./development/setup.md)** - How to set up local environment
- **[Testing](./development/testing.md)** - Automated and manual testing
- **[Contributing](./development/contributing.md)** - Guide for contributors

## Project Overview

Little Lemon is a complete restaurant management system that includes:

- **Backend API**: Django REST Framework with JWT authentication
- **Frontend**: Responsive web interface using Django templates
- **Infrastructure**: AWS (Lambda, RDS, S3, CloudFront)
- **Database**: MySQL initially and RDS in the cloud

### System Actors

| Actor | Description | Main Permissions |
|-------|-------------|------------------|
| **Admin** | System administrator | Full access, user management |
| **Manager** | Restaurant manager | Order management, menu, staff |
| **Delivery Crew** | Delivery team | View and update assigned order status |
| **Customer** | End customer | Browse menu, place orders, booking tables |

### Quick Links

- [AWS Architecture](./assets/aws_architecture_-_little_lemon_project.png)
- [API Base URL](https://api.littlelemon.com) (Production)
- [Repository](https://github.com/Val-Cantarelli/Meta-AWS-Capstone)

---

**Last updated:** October 2025  
**API Version:** v1.0