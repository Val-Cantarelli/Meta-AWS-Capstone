# Frontend – Meta AWS Capstone

## Overview
Django-based customer interface for a restaurant platform, designed for cloud-native deployment on AWS Elastic Beanstalk. Implements Server-Side Rendering (SSR) for fast load and SEO, with limited functionality serving as a **demonstration** of frontend-API integration and AWS deployment patterns.

**⚠️ Note:** This is a **demo implementation** with basic functionality. Not suitable for production restaurant operations.

**Current Implementation Status:**
- **Implemented**: Menu browsing, user authentication (login/signup), table booking form (demo only - no backend API)
- **Missing**: Backend booking API, complete ordering system, cart management, order tracking, role-based interfaces
- **Purpose**: Demonstrates frontend-API integration and AWS deployment patterns

## Features
- **Demo customer interface**: menu browsing, authentication, table booking form
- Server-Side Rendering (SSR) for SEO and fast initial load
- JWT authentication integration with backend API
- AWS Elastic Beanstalk deployment with health checks
- Static/media assets served from S3

**Important:** This is a demonstration frontend with limited functionality.

## Project Structure
- `ui_app/` – Django app (views, templates, static);
- `core/` – Project settings, ASGI entrypoints;
- `.ebextensions`, `.elasticbeanstalk`,`.platform`, – Custom Elastic Beanstalk and Nginx configuration used for deployment and health checks;
- `run-local.sh`, `run-prod.sh` – Local/prod scripts.

## Local Development
- Configure `.env` with `API_BASE_URL` (point to API Gateway or local backend), `DJANGO_SETTINGS_MODULE`, and secrets.
- Use `run-local.sh` for local dev; `run-prod.sh` for prod-like runs.
- All settings and secrets loaded from `.env` (**NEVER** commit to GitHub).

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



## Known Limitations & Future Work

**Current Issues:**
- Table booking form exists but backend API not implemented
- Limited error handling and user feedback
- Basic UI styling and user experience

**Planned Improvements:**
- Complete ordering system with cart management
- Role-based interfaces for managers and delivery crew
- Enhanced UX with loading states and better error messages
- Comprehensive testing and accessibility improvements

**For Development:**
- Monitor CloudWatch logs for errors and performance
- Ensure `CSRF_TRUSTED_ORIGINS` and `API_BASE_URL` alignment
- Maintain secure server-side JWT token storage

## Project Credits and Customizations

**Base Implementation:**
The core frontend (templates, static files, base views) was provided by the Meta course.

**Custom Development:**
- Authentication system integration (auth_views.py, auth_utils.py) 
- Login and signup templates and authentication flows
- Table booking demo form (UI only - backend API pending implementation)
- JWT token management with backend API
- AWS Elastic Beanstalk deployment configuration
- Production security settings and health checks
- Environment variable management and S3 integration

## References
- [Django Documentation](https://docs.djangoproject.com/ )
- [AWS Elastic Beanstalk](https://docs.aws.amazon.com/elasticbeanstalk/latest/dg/Welcome.html)

