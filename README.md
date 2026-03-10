# BookStore Microservices

A microservice-based bookstore built with **Django REST Framework**, **Docker Compose**, and independent databases.

## Architecture

| #   | Service                    | Port | Description                                             |
| --- | -------------------------- | ---- | ------------------------------------------------------- |
| 1   | **api-gateway**            | 8000 | Routes all client requests to downstream services       |
| 2   | **staff-service**          | 8001 | Staff user management (CRUD)                            |
| 3   | **manager-service**        | 8002 | Manager user management (CRUD)                          |
| 4   | **customer-service**       | 8003 | Customer registration (auto-creates cart) & login       |
| 5   | **catalog-service**        | 8004 | Book categories/catalogs                                |
| 6   | **book-service**           | 8005 | Book CRUD (managed by staff), search, stock             |
| 7   | **cart-service**           | 8006 | Shopping cart add/view/update/remove                    |
| 8   | **order-service**          | 8007 | Order creation (triggers payment & shipping)            |
| 9   | **ship-service**           | 8008 | Shipment tracking & status                              |
| 10  | **pay-service**            | 8009 | Payment processing & refunds                            |
| 11  | **comment-rate-service**   | 8010 | Book ratings & comments                                 |
| 12  | **recommender-ai-service** | 8011 | AI-based book recommendations (collaborative filtering) |

## Quick Start

```bash
docker-compose up --build
```

## API Endpoints (via Gateway at port 8000)

### Customers

- `POST /api/customers/register/` — Register (auto-creates cart)
- `POST /api/customers/login/`
- `GET /api/customers/`

### Books

- `GET /api/books/` — List all books
- `POST /api/books/` — Create book (staff)
- `GET /api/books/{id}/`
- `GET /api/books/search/?q=keyword`
- `GET /api/books/by_catalog/?catalog_id=1`

### Cart

- `GET /api/carts/by_customer/?customer_id=1` — View cart
- `POST /api/carts/add_item/` — Add book to cart `{customer_id, book_id, quantity}`
- `PUT /api/carts/update_item/` — Update quantity `{customer_id, book_id, quantity}`
- `DELETE /api/carts/remove_item/?customer_id=1&book_id=1`

### Orders

- `POST /api/orders/create_from_cart/` — Create order `{customer_id, payment_method, shipping_method, shipping_address}`
- `GET /api/orders/by_customer/?customer_id=1`
- `POST /api/orders/{id}/cancel/`

### Payments

- `GET /api/payments/by_order/?order_id=1`
- `POST /api/payments/{id}/process/`
- `POST /api/payments/{id}/refund/`

### Shipping

- `GET /api/shipments/by_order/?order_id=1`
- `GET /api/shipments/track/?tracking_number=SHIP-XXXX`
- `POST /api/shipments/{id}/update_status/` — `{status: "shipped"}`

### Comments & Ratings

- `POST /api/comments/` — `{customer_id, book_id, rating, comment}`
- `GET /api/comments/by_book/?book_id=1`
- `GET /api/comments/by_customer/?customer_id=1`

### Recommendations

- `GET /api/recommendations/?customer_id=1&top_n=5`

### Catalogs

- `GET /api/catalogs/`
- `POST /api/catalogs/` — `{name, description}`

### Staff & Managers

- `GET /api/staff/`
- `POST /api/staff/`
- `GET /api/managers/`
- `POST /api/managers/`

## Inter-Service Communication

All communication between services is done via **REST HTTP calls** using Python `requests` library:

- **customer-service → cart-service**: Auto-create cart on registration
- **order-service → cart-service**: Fetch cart items
- **order-service → book-service**: Fetch prices, update stock
- **order-service → pay-service**: Create payment
- **order-service → ship-service**: Create shipment
- **cart-service → book-service**: Enrich cart items with book details
- **recommender-ai-service → comment-rate-service**: Fetch all ratings
- **recommender-ai-service → book-service**: Fetch book details
- **api-gateway → all services**: Proxy HTTP requests

## Technical Stack

- **Framework**: Django REST Framework
- **Inter-service**: REST HTTP (requests library)
- **Containerization**: Docker + Docker Compose
- **Databases**: Independent SQLite per service
- **AI**: Collaborative filtering (recommender-ai-service)
