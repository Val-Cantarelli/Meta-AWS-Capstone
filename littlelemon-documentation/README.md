## API Permissions & Access Rules

### Menu Items (`/api/menu-items`)
- **GET (list/retrieve):** Public
- **POST/PUT/PATCH/DELETE:** Only authenticated users

---

### Cart (`/api/cart/menu-items`)
- **GET/POST/DELETE:** Only authenticated users of type "customer" (not manager or delivery crew)
- Each user can only view and manage their own cart

---

### Orders (`/api/orders`)
- **GET (list):**
    - **Manager:** Can view all orders
    - **Delivery crew:** Can view only orders assigned to them
    - **Regular user:** Can view only their own orders
- **GET (retrieve):**
    - **Manager:** Can view any order
    - **Delivery crew:** Can view orders assigned to them
    - **Regular user:** Can view only their own orders
- **PATCH (partial_update):**
    - **Manager:** Can update any order
    - **Delivery crew:** Can update status of orders assigned to them
    - **Regular user:** Cannot update orders
- **POST (create):** Only authenticated users (creates order from their own cart)
- **DELETE:** (If implemented) Manager only

---

### Manager Group (`/api/groups/manager/users`)
- **GET/POST/DELETE:** Only admin or manager can add/remove users from the manager group

---

### Delivery Crew Group (`/api/groups/delivery-crew/users`)
- **GET/POST/DELETE:** Only admin or manager can add/remove users from the delivery crew group

---

## Notes

- **Authentication:** JWT required for protected endpoints.
- **Custom permissions:** Implemented via classes such as `IsAdminOrManager`, `IsCustomer`, etc.
- **Pagination:** Enabled on listing endpoints (e.g., menu-items, orders).
