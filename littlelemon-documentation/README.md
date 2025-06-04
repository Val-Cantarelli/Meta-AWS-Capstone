## API Permissions & Access Rules

There is four actors: admin, manager, delivery-crew and customer

### Menu Items (`/api/menu-items`)
- **GET:** Public
- **POST/PUT/DELETE:** Only admin users
- **PATCH:** Manager (especificaly at fields "featured(prato do dia) and availability")
---

### Cart (`/api/cart/menu-items`)
- **GET/POST/DELETE (Manager):** Can view and manage all carts
- **GET/POST/DELETE (User):** Can view and manage only their own cart
---

### Orders (`/api/orders`)
- **GET/PATCH/POST/DELETE (Manager):** any order
- **GET (Delivery crew):** Can view only orders assigned to them
- **GET (Regular user):** Can view only their own orders
- **PATCH (Delivery crew):** Can update status of orders assigned to them
- **POST (Regular user):** Creates order from their own cart
---

### Manager Group (`/api/groups/manager/users`)
- **GET:** Admin or manager 
- **POST/DELETE:** Only admin can add/remove users from the manager group
---

### Delivery Crew Group (`/api/groups/delivery-crew/users`)
- **GET/POST/DELETE:** Admin or manager can add/remove users from the delivery crew group

---

## Notes

- **Authentication:** JWT required for protected endpoints.
- **Custom permissions:** Implemented via classes such as `IsAdminOrManager`, `IsCustomer`, etc.
- **Pagination:** Enabled on listing endpoints (e.g., menu-items, orders).




## Business Rules

- Only admin can create new menu items to ensure menu integrity and security.
- This may be revised in the future to allow manager proposals with admin approval.