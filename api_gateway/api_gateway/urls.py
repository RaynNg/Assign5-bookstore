from django.urls import path
from . import views

urlpatterns = [
    # Customer API
    path("api/customers/", views.customers),
    path("api/customers/login/", views.customer_login),
    path("api/customers/<int:pk>/", views.customer_detail),
    # Book API
    path("api/books/", views.books),
    path("api/books/<int:pk>/", views.book_detail),
    # Cart API
    path("api/carts/", views.carts),
    path("api/carts/<int:pk>/", views.cart_detail),
    path("api/carts/customer/<int:customer_id>/", views.cart_by_customer),
    path("api/cart-items/", views.cart_items),
    path("api/cart-items/<int:pk>/", views.cart_item_detail),
    path("api/carts/<int:customer_id>/items/", views.view_cart_items),
    path("api/carts/<int:customer_id>/clear/", views.clear_cart),
    # Staff API
    path("api/staff/", views.staff),
    path("api/staff/login/", views.staff_login),
    path("api/staff/<int:pk>/", views.staff_detail),
    path("api/staff/manage-book/", views.staff_manage_book),
    path("api/staff/manage-book/<int:book_id>/", views.staff_manage_book_detail),
    # Manager API
    path("api/managers/", views.managers),
    path("api/managers/<int:pk>/", views.manager_detail),
    # Catalog API
    path("api/categories/", views.categories),
    path("api/categories/<int:pk>/", views.category_detail),
    path("api/catalog/", views.catalog),
    # Order API
    path("api/orders/", views.orders),
    path("api/orders/<int:pk>/", views.order_detail),
    path("api/orders/checkout/", views.checkout),
    path("api/orders/customer/<int:customer_id>/", views.customer_orders),
    # Ship API
    path("api/shipments/", views.shipments),
    path("api/shipments/<int:pk>/", views.shipment_detail),
    path("api/shipping-methods/", views.shipping_methods),
    # Pay API
    path("api/payments/", views.payments),
    path("api/payments/<int:pk>/", views.payment_detail),
    path("api/payment-methods/", views.payment_methods),
    # Review/Rating API
    path("api/reviews/", views.reviews),
    path("api/reviews/<int:pk>/", views.review_detail),
    path("api/books/<int:book_id>/reviews/", views.book_reviews),
    path("api/books/<int:book_id>/rating/", views.book_rating),
    # Recommender API
    path("api/recommendations/<int:customer_id>/", views.recommendations),
    path("api/similar/<int:book_id>/", views.similar_books),
    path("api/popular/", views.popular_books),
    path("api/trending/", views.trending_books),
]
