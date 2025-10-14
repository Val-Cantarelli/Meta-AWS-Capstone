# Backend — Django REST API 

Production-ready REST API for a restaurant management system, designed as the core of an API-first architecture. Features JWT authentication, role-based access control, comprehensive cart and order management, and cloud-native AWS deployment capabilities.

This document provides a comprehensive overview of the backend architecture, setup, and key features.

## Stack
- Python 3.11
- Django (project core)
- Django REST Framework (DRF)
- Djoser + SimpleJWT (JWT auth)
- drf-spectacular (OpenAPI 3.0 documentation)
- django-filter (filters)
- Additional renderers: XML, CSV, YAML
- Database: SQLite (local), MySQL (production via RDS + RDS Proxy)

Key paths:
- App: `LittleLemon/LittleLemonAPI`
- Root URLs: `LittleLemon/LittleLemon/urls.py`
- Models/Views/Serializers: in `LittleLemon/LittleLemonAPI/`
- Settings: `LittleLemon/LittleLemon/settings/` (`base.py`, `production.py`)

## Architecture and Design Rationale
This API is designed around DRF viewsets exposing clear resources (menu, categories, cart, orders) with stateless JWT authentication. Role-based access control uses Django Groups to keep authorization simple and auditable: managers curate the menu and orchestrate orders; delivery crew handle fulfillment; customers place orders. Pagination, filtering, and throttling are enabled by default to protect the API, bound query costs, and provide a consistent client experience.

In production, configuration and secrets are externalized (SSM Parameter Store for SECRET_KEY, Secrets Manager for DB credentials). RDS Proxy smooths connection spikes and improves resilience for serverless or autoscaled runtimes. The service can run behind API Gateway + Lambda (with a lightweight ASGI/WSGI adapter) or on Elastic Beanstalk behind an ALB. Health checks are explicit to keep infrastructure feedback loops reliable.

## Data Models
- Category: slug, title
- MenuItem: title, price, featured, availability, category (FK)
- Cart: user, menuitem, quantity, unit_price, price (unique per user+item)
- Order: user, delivery_crew (User), status (bool), total, date
- OrderItem: order, menuitem, quantity, unit_price, price (unique per order+item)

## How the main flows work
- Browse menu: anonymous users can list and search menu items using indexed fields (title, category, price) with pagination to minimize payloads.
- Sign up and log in: Djoser issues JWTs; the client includes the access token on subsequent requests. Refresh tokens extend sessions without re-authenticating.
- Cart to order: a customer adds items to the cart; creating an order snapshots prices/quantities into OrderItem and clears the cart to avoid accidental reorders.
- Order orchestration: a manager assigns a delivery crew member and updates status; delivery crew can update status during fulfillment. Access to orders is restricted by role (own, assigned, or all for managers).

## Authentication & Authorization

The API uses JWT authentication via Djoser with role-based access control through Django Groups:

- **JWT Authentication**: Stateless token-based auth with access/refresh tokens
- **Role-based Access**: Manager, Delivery Crew, and Customer roles
- **Group Management**: Admin and Manager can assign users to groups

**Quick Overview:**
- `POST /auth/jwt/create` - Login (get access token)
- `POST /auth/jwt/refresh` - Refresh access token  
- `POST /auth/users/` - User registration

## API Endpoints & Permissions

**Core Resources:**
- **Menu Items** - Public browsing, admin/manager management
- **Categories** - Public listing, admin management  
- **Cart** - Customer cart management (add, update, remove items)
- **Orders** - Role-based order workflow (create, assign, fulfill)
- **User Groups** - Manager/admin user role management

**Permission Summary:**
- **Managers**: Full menu management, order orchestration, user group assignment
- **Delivery Crew**: View assigned orders, update delivery status
- **Customers**: Browse menu, manage cart, create and view own orders
- **Anonymous**: Browse menu items and categories

## API Features

**Search & Filtering:**
- Menu items: filter by category, price; search by title; ordering by price
- Pagination: 3 items per page (configurable)

**Content Negotiation:**
- Multiple formats: JSON (default), XML, CSV, YAML
- Request via `Accept` header (e.g., `Accept: application/xml`)

**Rate Limiting:**
- Anonymous users: 20 requests/minute  
- Authenticated users: 100 requests/minute

**Health Check:**
- `GET /health` → `{ "status": "ok" }` (for load balancer health checks)

**OpenAPI Documentation:**
- Auto-generated schema via drf-spectacular
- Interactive docs available at `/api/schema/swagger-ui/`
- Complete OpenAPI 3.0 schema: `openapi-schema.yaml`

## Local Development
Prereqs: Python 3.11 and Pipenv.

1) Install deps
- In `backend/`:
  - `pipenv install`
  - optionally: `pipenv install --dev`
2) Activate env: `pipenv shell`
3) Migrate local sqlite DB: `python manage.py migrate`
4) Create superuser: `python manage.py createsuperuser`
5) Run: `python manage.py runserver`

Notes:
- `manage.py` uses `DJANGO_ENV` (default: `local`) to select settings: `LittleLemon.LittleLemon.settings.{ENV}`
- To override, export: `export DJANGO_ENV=base` or use script `manage_local.sh`

## Django Admin
- URL: `/admin`
- Create superuser: `python manage.py createsuperuser`
- Models available: Category, MenuItem, Cart, Order (register OrderItem if you want to administer items per order)
- Groups: create `manager` and `delivery-crew` and assign users accordingly
- Production hygiene: restrict access, use strong passwords/2FA, consider changing the admin path and applying IP allowlists

## Production (AWS)
- Settings: `LittleLemon/LittleLemon/settings/production.py`
- Required environment variables:
  - `DB_NAME`: schema name
  - `DB_HOST`: RDS Proxy endpoint (e.g., `xxxx.proxy-...rds.amazonaws.com`)
  - `DB_SECRET_NAME`: Secrets Manager secret (with `username` and `password`)
  - `DJANGO_SECRET_PARAM`: SSM Parameter Store name holding `SECRET_KEY`
  - `AWS_REGION`: region (default us-east-1)
- Integrations:
  - Secrets Manager: DB credentials (`utils/aws.py:get_db_credentials`)
  - SSM Parameter Store: SECRET_KEY
  - MySQL via `pymysql`
- ALLOWED_HOSTS: include your API Gateway/EB host. Example present: `6qpkzrhv4c.execute-api.us-east-1.amazonaws.com`
- API Gateway (optional): if using stage `/v1`, tweak pagination to rewrite links (commented in `production.py`).

## Operations and Observability
- Health checks: `/health` endpoint responds 200 for load balancers
- Logging: rely on platform logs (EB/ALB or API Gateway/Lambda + CloudWatch) for request tracing and error diagnostics
- Migrations: run `python manage.py migrate` on deploys that change the schema
- Rate limits: DRF throttling protects against bursts; tune per environment
- Secrets and config: never hardcode; use environment and managed secret stores

## Future Work
- **Role-based frontend interfaces**: Implement dedicated views for Manager, Delivery Crew, and Admin roles with tailored dashboards and workflows
- **Observability**: Structured logging, request IDs, and performance metrics
- **Performance optimization**: Selective prefetching and caching for high-traffic endpoints
- **Enhanced security**: Comprehensive permission testing and audit logging
- **API versioning**: Implement versioning strategy for backward compatibility

## Credits and Customizations
- Based on Meta Backend (Little Lemon) coursework. Major adaptations:
  - **Architecture**: Migrated from function-based views to DRF ViewSets for better organization and functionality
  - **Authentication**: JWT auth with Djoser and group-based permissions (replacing session auth)
  - **API Features**: Filters/search/ordering on Menu Items; standardized pagination
  - **Content Types**: Extra renderers (XML/CSV/YAML) beyond JSON
  - **Monitoring**: Health check `/health` endpoint
  - **Cloud Integration**: AWS SSM for SECRET_KEY, Secrets Manager for DB, RDS Proxy, production `ALLOWED_HOSTS`
  - **Performance**: DRF rate limiting and throttling
