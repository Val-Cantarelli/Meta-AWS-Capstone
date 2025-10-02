# API Endpoints Documentation

## API Status
- **Production Ready**: All endpoints implemented and tested
- **Frontend Agnostic**: Can be consumed by any client application
- **Secure**: JWT authentication with role-based permissions

## Base URL
```
Production: https://api.littlelemon.com
Development: http://localhost:8000
```

## Endpoints Index

- [Menu Items](#menu-items)
- [Cart Management](#cart-management) 
- [Orders](#orders)
- [User Groups](#user-groups)
- [Authentication](#authentication)

---

## Menu Items

### `GET /api/menu-items`
**Access:** Public (no authentication required)

Lists all menu items with support for filters, search, and pagination.

#### Query Parameters
| Parameter | Type | Description | Example |
|-----------|------|-------------|---------|
| `search` | string | Search by title or category | `?search=pizza` |
| `category` | string | Filter by category | `?category=main-course` |
| `featured` | boolean | Featured items only | `?featured=true` |
| `ordering` | string | Order by price | `?ordering=price` or `?ordering=-price` |
| `page` | number | Pagination page | `?page=2` |

#### Response
```json
{
  "count": 25,
  "next": "http://localhost:8000/api/menu-items/?page=2",
  "previous": null,
  "results": [
    {
      "id": 1,
      "title": "Margherita Pizza",
      "price": "15.99",
      "featured": true,
      "category": 1
    }
  ]
}
```

### `POST /api/menu-items`
**Access:** Admin only

Creates a new menu item.

#### Request Body
```json
{
  "title": "Quattro Stagioni",
  "price": "18.99",
  "featured": false,
  "category": 1
}
```

### `PATCH /api/menu-items/{id}`
**Access:** Manager

Updates specific fields (mainly `featured`).
- **`featured`**: Mark/unmark item as "today's special" (featured menu item)

#### Request Body
```json
{
  "featured": true
}
```

### `DELETE /api/menu-items/{id}`
**Access:** Admin only

Removes a menu item.

---

## Cart Management

### `GET /api/cart`
**Access:** Customer only

- **Customer:** Views only their own cart

#### Response
```json
[
  {
    "id": 1,
    "menuitem_name": "Margherita Pizza",
    "menuitem": 1,
    "quantity": 2,
    "price": "31.98"
  }
]
```

### `POST /api/cart`
**Access:** Customer

Adds item to cart.

#### Request Body
```json
{
  "menuitem": 1,
  "quantity": 2
}
```

### `PATCH /api/cart/{id}`
**Access:** Customer (own cart)

Updates item quantity.

#### Request Body
```json
{
  "quantity": 3
}
```

### `DELETE /api/cart/{id}`
**Access:** Customer (own cart only)

Removes item from cart.

---

## Orders

### `GET /api/orders`
**Access:** Authenticated Users

- **Manager:** All orders
- **Delivery Crew:** Only assigned orders
- **Customer:** Only their own orders

#### Response
```json
{
  "count": 15,
  "results": [
    {
      "id": 1,
      "user": 2,
      "delivery_crew": 3,
      "status": false,
      "total": "47.97",
      "date": "2025-10-01",
      "items": [
        {
          "menuitem": 1,
          "menuitem_title": "Margherita Pizza",
          "quantity": 2,
          "unit_price": "15.99",
          "price": "31.98"
        }
      ]
    }
  ]
}
```

### `POST /api/orders`
**Access:** Customer

Creates order from cart items.

#### Response
```json
{
  "order_id": 1,
  "total": "47.97",
  "items": [
    {
      "menuitem": "Margherita Pizza",
      "quantity": 2,
      "unit_price": "15.99",
      "price": "31.98"
    }
  ],
  "detail": "Order created!"
}
```

### `PATCH /api/orders/{id}`
**Access:** Manager (all orders) | Delivery Crew (assigned orders) | Admin

Updates order status or assigns delivery crew.

#### Request Body (Manager)
```json
{
  "delivery_crew": 3,
  "status": true
}
```

#### Request Body (Delivery Crew)
```json
{
  "status": true
}
```

---

## User Groups

### `GET /api/groups/{group_name}/users`
**Access:** Admin or Manager

Lists users in a specific group.

**Available groups:** `manager`, `delivery-crew`

#### Response
```json
[
  {
    "id": 2,
    "username": "manager1",
    "email": "manager@littlelemon.com"
  }
]
```

### `POST /api/groups/{group_name}/users`
**Access:** Admin (for managers) | Admin or Manager (for delivery-crew)

Adds user to a group.

#### Request Body
```json
{
  "username": "new_manager"
}
```

### `DELETE /api/groups/{group_name}/users/{user_id}`
**Access:** Admin (for managers) | Admin or Manager (for delivery-crew)

Removes user from a group.

---

## Authentication

> ** Complete Documentation:** See [authentication.md](authentication.md) for detailed JWT implementation

### Quick Reference

#### `POST /auth/users/`
Registers new user.

#### `POST /auth/jwt/create/`
Generates JWT token.

#### Request Body
```json
{
  "username": "user@example.com",
  "password": "password123"
}
```

#### Response
```json
{
  "access": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```

#### `POST /auth/jwt/refresh/`
Refreshes JWT token.

---

## Status Codes

| Code | Description |
|------|-----------|
| 200 | Success |
| 201 | Created successfully |
| 400 | Bad Request |
| 401 | Unauthorized |
| 403 | Permission denied |
| 404 | Not found |
| 429 | Rate limit exceeded |

## Required Headers

```http
Authorization: Bearer {access_token}
Content-Type: application/json
```

## Testing

**Recommended Tools:**
- **Postman**: Import collection for comprehensive API testing
- **Insomnia**: Alternative REST client
- **Django Admin**: Content management at `/admin/`
- **API Browser**: DRF browsable API for development









