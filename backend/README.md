# Backend — Django REST API 

REST API for a restaurant management system with JWT authentication, group-based access control (manager, delivery-crew, customer), cart, and orders. Ready for local development and AWS deployment (API Gateway + Lambda or Elastic Beanstalk + RDS).

## Stack
- Python 3.11
- Django (project core)
- Django REST Framework (DRF)
- Djoser + SimpleJWT (JWT auth)
- django-filter (filters)
- Additional renderers: XML, CSV, YAML
- Database: MySQL (production via RDS + RDS Proxy)

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

## Authentication
- JWT via Djoser + SimpleJWT
- Djoser endpoints under `/auth/`:
  - POST `/auth/jwt/create` (username, password)
  - POST `/auth/jwt/refresh`
  - POST `/auth/jwt/verify`
  - POST `/auth/users/` (user registration)
- Config: `REST_FRAMEWORK.DEFAULT_AUTHENTICATION_CLASSES = JWTAuthentication`

## Groups and Permissions
- manager: can manage menu, categories, and assign delivery crew to orders
- delivery-crew: can view assigned orders and update their status
- customer (authenticated user not in manager or delivery-crew): can use cart and create orders

Per resource:
- Categories (`/api/categories`):
  - GET: authenticated
  - POST/PUT/PATCH/DELETE: admin
- Menu (`/api/menu-items`):
  - GET/GET {id}: public
  - POST/DELETE: admin
  - PUT/PATCH: manager
- Groups (`/api/groups/(manager|delivery-crew)/users`): admin or manager
  - GET list, POST add `username`
  - DELETE `/api/groups/{group}/users/{id}` remove user from group
- Cart (`/api/cart`): authenticated + customer
  - GET: current user items
  - POST: add item `{menuitem, quantity}`
  - PATCH `/api/cart/{id}`: update quantity
  - DELETE `/api/cart/{id}`: remove item
- Orders (`/api/orders`): authenticated
  - manager: sees all
  - delivery-crew: sees assigned
  - customer: sees own
  - GET list/detail; POST creates from cart; PATCH updates (manager can set `delivery_crew` and `status`; delivery-crew can change `status`)

Health Check:
- GET `/health` → `{ "status": "ok" }`

## Main Endpoints
Base: `/api/`

- Menu Items
  - GET `/api/menu-items?category={slug}&price={num}&search={q}&ordering=price|-price&page=N`
  - POST `/api/menu-items`
  - GET `/api/menu-items/{id}`
  - PATCH/PUT/DELETE `/api/menu-items/{id}`
- Categories
  - GET `/api/categories`
  - POST `/api/categories`
  - GET `/api/categories/{id}`
  - PATCH/PUT/DELETE `/api/categories/{id}`
- Groups (Managers / Delivery Crew)
  - GET `/api/groups/manager/users`
  - POST `/api/groups/manager/users` body: `{ "username": "john" }`
  - DELETE `/api/groups/manager/users/{userId}`
  - (same for `delivery-crew`)
- Cart
  - GET `/api/cart`
  - POST `/api/cart` body: `{ "menuitem": 1, "quantity": 2 }`
  - PATCH `/api/cart/{id}` body: `{ "quantity": 3 }`
  - DELETE `/api/cart/{id}`
- Orders
  - GET `/api/orders`
  - GET `/api/orders/{id}`
  - POST `/api/orders`
  - PATCH `/api/orders/{id}` body (manager): `{ "delivery_crew": 5, "status": true }`

## Filtering, Search, Ordering, Pagination
- On `/api/menu-items`:
  - Filters: `category` (slug, iexact), `price` (exact)
  - Search: `search=title|category__slug|id`
  - Ordering: `ordering=price` or `ordering=-price`
- Pagination: PageNumber, `PAGE_SIZE=3` → use `?page=2`

## Supported Renderers
- JSON (default), Browsable API, XML, CSV, YAML
- Content negotiation via `Accept` header (e.g., `Accept: application/xml`)

## Throttling
- Anon and User: 10/min (`DEFAULT_THROTTLE_RATES`)

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

## Frontend Coverage and Manual Testing
Some API capabilities are not exposed in the web UI. Use Insomnia or curl to exercise them directly:

- Categories: POST/PUT/PATCH/DELETE (admin only)
- Groups: `/api/groups/(manager|delivery-crew)/users` to list, add by `username`, and remove by `userId` (admin or manager)
- Orders: `PATCH /api/orders/{id}` to assign `delivery_crew` or change `status` (manager/delivery-crew)
- Cart: `PATCH` and `DELETE /api/cart/{id}` to update/remove specific items
- Menu Items: admin-only create/delete

Examples (requires JWT in Authorization header):
- Assign delivery crew to an order (manager):
  `curl -X PATCH /api/orders/123 -H "Authorization: Bearer <token>" -H "Content-Type: application/json" -d '{"delivery_crew": 5, "status": true}'`
- Add user to manager group (manager/admin):
  `curl -X POST /api/groups/manager/users -H "Authorization: Bearer <token>" -H "Content-Type: application/json" -d '{"username":"john"}'`

## Quick Tests (curl)
- Login: `curl -X POST /auth/jwt/create -d '{"username":"admin","password":"..."}' -H 'Content-Type: application/json'`
- Public menu: `curl /api/menu-items`
- Cart (with JWT): `curl -H 'Authorization: Bearer <token>' /api/cart`

## Future Work
- Admin UX: register `OrderItem` and add list filters/search to ease operations
- Observability: add request IDs, structured logging, and basic metrics (latency, error rate)
- Performance: add selective prefetching and caching for hot endpoints
- Security: add permission tests and audit logs for group changes
- Product: align booking workflow with backend API once finalized

## Credits and Customizations
- Based on Meta Backend (Little Lemon) coursework. Adaptations:
  - JWT auth with Djoser and group-based permissions
  - Filters/search/ordering on Menu Items; standardized pagination
  - Extra renderers (XML/CSV/YAML)
  - Health check `/health`
  - AWS integration: SSM for SECRET_KEY, Secrets Manager for DB, RDS Proxy, `ALLOWED_HOSTS` adjustments
  - DRF rate limiting
