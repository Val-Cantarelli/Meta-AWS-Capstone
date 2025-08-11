# Frontend – Meta AWS Capstone

## Overview
Production-ready Django frontend for a restaurant platform, designed for cloud-native deployment on AWS Elastic Beanstalk. Implements Server-Side Rendering (SSR) for fast load, SEO, and robust integration with a JWT-authenticated API.

## Features
- Modular Django templates: home, menu,booking, login, signup.
- JWT authentication via API Gateway.
- Organized views for menu, auth, and base flows.
- Static/media assets offloaded to S3.

## Project Structure
- `ui_app/` – Django app (views, templates, static);
- `core/` – Project settings, ASGI entrypoints;
- `.ebextensions`, `.elasticbeanstalk`,`.platform`, – Custom Elastic Beanstalk and Nginx configuration used for deployment and health checks;
- `run-local.sh`, `run-prod.sh` – Local/prod scripts.

## Local Development
- Configure `.env` with `API_BASE_URL` (point to API Gateway or local backend), `DJANGO_SETTINGS_MODULE`, and secrets.
- Use `run-local.sh` for local dev; `run-prod.sh` for prod-like runs.
- All settings and secrets loaded from `.env` (NEEVER commit to hte GitHub).

## Deployment (Frontend on Elastic Beanstalk)
- Runtime: ASGI with Gunicorn + Uvicorn (see `frontend/Procfile`).
- Health checks: Nginx returns 200 for `/health` and `/health/` via snippet at `frontend/.platform/nginx/conf.d/elasticbeanstalk/99_health.conf`.
  - Target Group and EB Health are configured to use path `/health` over HTTP 80.
- Environment variables (examples):
  - `DJANGO_SETTINGS_MODULE=core.settings.production`
  - `API_BASE_URL=<your_api_gateway_url>`
  - `AWS_STORAGE_BUCKET_NAME=<bucket>`
  - `AWS_S3_REGION_NAME=us-east-1` (default)
  - `DJANGO_SECRET_KEY=<secret>`
- Static/media: served from S3 via `django-storages`.

## Security
- HTTPS at ALB with ACM certificate and HTTP→HTTPS redirect for users.
- Django production settings: `SECURE_PROXY_SSL_HEADER`, `USE_X_FORWARDED_HOST`, `SECURE_SSL_REDIRECT`.
- Cookies: `SESSION_COOKIE_SECURE`, `CSRF_COOKIE_SECURE`.
- CSRF: `CSRF_TRUSTED_ORIGINS` configured for domains.
- Health endpoint exempt from redirect to keep targets healthy.

**How authentication works:**
JWT tokens (access/refresh) are stored in the Django session on the server side. The browser only keeps a session cookie; tokens are never exposed directly to the client. This ensures secure API calls and avoids leaking sensitive credentials.

## SSR and SEO
All pages are rendered server-side using Django templates. This guarantees fast initial load and makes content fully indexable by search engines, improving SEO and accessibility.

## Health checks
- `/health` is served by Nginx (not Django) to avoid HTTPS redirects and app overhead.
- Target Group success codes set to 200 (tolerant 200–399 during transition if needed).

## Extensibility
- Views and templates organized for easy feature addition.
- API integration via settings; swap endpoints without code change.

## Troubleshooting
- Health check failures: verify Nginx snippet and TG path.
- CSRF/auth issues: check trusted origins and API_BASE_URL.
- Static/media: confirm S3 bucket and permissions.

## Project credits and customizations

The core frontend (templates, static files, base views) was provided by the Meta course.
- Custom work:
  - Implemented auth_views.py for authentication flows.
  - Created/modified login and signup templates.
  - Developed auth_utils.py for JWT integration with the API Gateway.
  - Adapted and extended configuration for Elastic Beanstalk deployment, API Gateway connectivity, and JWT authentication.

Additional changes: adjusted environment variables, health checks, and security settings to support production deployment on AWS.

## References
- [Django Documentation](https://docs.djangoproject.com/ )
- [AWS Elastic Beanstalk](https://docs.aws.amazon.com/elasticbeanstalk/latest/dg/Welcome.html)
- [API Gateway](https://docs.aws.amazon.com/apigateway/)

