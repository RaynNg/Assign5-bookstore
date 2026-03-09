from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import requests
import json

# Service URLs
CUSTOMER_SERVICE_URL = "http://customer-service:8000"
BOOK_SERVICE_URL = "http://book-service:8000"
CART_SERVICE_URL = "http://cart-service:8000"
STAFF_SERVICE_URL = "http://staff-service:8000"
MANAGER_SERVICE_URL = "http://manager-service:8000"
CATALOG_SERVICE_URL = "http://catalog-service:8000"
ORDER_SERVICE_URL = "http://order-service:8000"
SHIP_SERVICE_URL = "http://ship-service:8000"
PAY_SERVICE_URL = "http://pay-service:8000"
COMMENT_SERVICE_URL = "http://comment-rate-service:8000"
RECOMMENDER_SERVICE_URL = "http://recommender-ai-service:8000"


# Customer endpoints
@csrf_exempt
def customers(request):
    return proxy_request(CUSTOMER_SERVICE_URL, "customers/", request)


@csrf_exempt
def customer_login(request):
    """Customer login"""
    return proxy_request(CUSTOMER_SERVICE_URL, "customers/login/", request)


@csrf_exempt
def customer_detail(request, pk):
    return proxy_request(CUSTOMER_SERVICE_URL, f"customers/{pk}/", request)


# Book endpoints
@csrf_exempt
def books(request):
    return proxy_request(BOOK_SERVICE_URL, "books/", request)


@csrf_exempt
def book_detail(request, pk):
    return proxy_request(BOOK_SERVICE_URL, f"books/{pk}/", request)


# Cart endpoints
@csrf_exempt
def carts(request):
    return proxy_request(CART_SERVICE_URL, "carts/", request)


@csrf_exempt
def cart_detail(request, pk):
    return proxy_request(CART_SERVICE_URL, f"carts/{pk}/", request)


@csrf_exempt
def cart_by_customer(request, customer_id):
    return proxy_request(CART_SERVICE_URL, f"carts/customer/{customer_id}/", request)


@csrf_exempt
def cart_items(request):
    return proxy_request(CART_SERVICE_URL, "cart-items/", request)


@csrf_exempt
def cart_item_detail(request, pk):
    return proxy_request(CART_SERVICE_URL, f"cart-items/{pk}/", request)


@csrf_exempt
def view_cart_items(request, customer_id):
    """Customer views their cart items"""
    return proxy_request(CART_SERVICE_URL, f"carts/{customer_id}/items/", request)


@csrf_exempt
def clear_cart(request, customer_id):
    """Customer clears their cart"""
    return proxy_request(CART_SERVICE_URL, f"carts/{customer_id}/clear/", request)


# Staff endpoints
@csrf_exempt
def staff(request):
    return proxy_request(STAFF_SERVICE_URL, "staff/", request)


@csrf_exempt
def staff_login(request):
    """Staff login"""
    return proxy_request(STAFF_SERVICE_URL, "staff/login/", request)


@csrf_exempt
def staff_detail(request, pk):
    return proxy_request(STAFF_SERVICE_URL, f"staff/{pk}/", request)


@csrf_exempt
def staff_manage_book(request):
    """Staff creates a new book"""
    return proxy_request(STAFF_SERVICE_URL, "staff/manage-book/", request)


@csrf_exempt
def staff_manage_book_detail(request, book_id):
    """Staff updates or deletes a book"""
    return proxy_request(STAFF_SERVICE_URL, f"staff/manage-book/{book_id}/", request)


# Manager endpoints
@csrf_exempt
def managers(request):
    return proxy_request(MANAGER_SERVICE_URL, "managers/", request)


@csrf_exempt
def manager_detail(request, pk):
    return proxy_request(MANAGER_SERVICE_URL, f"managers/{pk}/", request)


# Catalog endpoints
@csrf_exempt
def categories(request):
    return proxy_request(CATALOG_SERVICE_URL, "categories/", request)


@csrf_exempt
def category_detail(request, pk):
    return proxy_request(CATALOG_SERVICE_URL, f"categories/{pk}/", request)


@csrf_exempt
def catalog(request):
    return proxy_request(CATALOG_SERVICE_URL, "catalog/", request)


# Order endpoints
@csrf_exempt
def orders(request):
    return proxy_request(ORDER_SERVICE_URL, "orders/", request)


@csrf_exempt
def order_detail(request, pk):
    return proxy_request(ORDER_SERVICE_URL, f"orders/{pk}/", request)


@csrf_exempt
def checkout(request):
    """POST - Create order from cart, trigger payment & shipping"""
    return proxy_request(ORDER_SERVICE_URL, "orders/checkout/", request)


@csrf_exempt
def customer_orders(request, customer_id):
    return proxy_request(ORDER_SERVICE_URL, f"orders/customer/{customer_id}/", request)


# Ship endpoints
@csrf_exempt
def shipments(request):
    return proxy_request(SHIP_SERVICE_URL, "shipments/", request)


@csrf_exempt
def shipment_detail(request, pk):
    return proxy_request(SHIP_SERVICE_URL, f"shipments/{pk}/", request)


@csrf_exempt
def shipping_methods(request):
    return proxy_request(SHIP_SERVICE_URL, "shipments/methods/", request)


# Pay endpoints
@csrf_exempt
def payments(request):
    return proxy_request(PAY_SERVICE_URL, "payments/", request)


@csrf_exempt
def payment_detail(request, pk):
    return proxy_request(PAY_SERVICE_URL, f"payments/{pk}/", request)


@csrf_exempt
def payment_methods(request):
    return proxy_request(PAY_SERVICE_URL, "payments/methods/", request)


# Comment/Rating endpoints
@csrf_exempt
def reviews(request):
    return proxy_request(COMMENT_SERVICE_URL, "reviews/", request)


@csrf_exempt
def review_detail(request, pk):
    return proxy_request(COMMENT_SERVICE_URL, f"reviews/{pk}/", request)


@csrf_exempt
def book_reviews(request, book_id):
    return proxy_request(COMMENT_SERVICE_URL, f"reviews/book/{book_id}/", request)


@csrf_exempt
def book_rating(request, book_id):
    return proxy_request(
        COMMENT_SERVICE_URL, f"reviews/book/{book_id}/rating/", request
    )


# Recommender endpoints
@csrf_exempt
def recommendations(request, customer_id):
    return proxy_request(
        RECOMMENDER_SERVICE_URL, f"recommendations/customer/{customer_id}/", request
    )


@csrf_exempt
def similar_books(request, book_id):
    return proxy_request(
        RECOMMENDER_SERVICE_URL, f"recommendations/similar/{book_id}/", request
    )


@csrf_exempt
def popular_books(request):
    return proxy_request(RECOMMENDER_SERVICE_URL, "recommendations/popular/", request)


@csrf_exempt
def trending_books(request):
    return proxy_request(RECOMMENDER_SERVICE_URL, "recommendations/trending/", request)
