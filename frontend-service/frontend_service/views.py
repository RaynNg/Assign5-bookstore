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


# HTML Views
def home(request):
    """Home page with featured books"""
    try:
        r = requests.get(f"{BOOK_SERVICE_URL}/books/")
        featured_books = r.json()[:4] if r.status_code == 200 else []
    except:
        featured_books = []
    return render(request, "index.html", {"featured_books": featured_books})


def book_list(request):
    try:
        r = requests.get(f"{BOOK_SERVICE_URL}/books/")
        books = r.json()
    except:
        books = []
    return render(request, "books.html", {"books": books})


def view_cart(request, customer_id=None):
    if customer_id is None:
        # Show empty cart if no customer specified
        return render(
            request,
            "cart.html",
            {"items": [], "subtotal": "0.00", "tax": "0.00", "total": "0.00"},
        )
    try:
        r = requests.get(f"{CART_SERVICE_URL}/carts/{customer_id}/items/")
        items = r.json() if r.status_code == 200 else []
        # Calculate totals
        subtotal = sum(float(item.get("subtotal", 0)) for item in items) if items else 0
        tax = subtotal * 0.08
        total = subtotal + 5.99 + tax
    except:
        items = []
        subtotal = tax = total = 0
    return render(
        request,
        "cart.html",
        {
            "items": items,
            "subtotal": f"{subtotal:.2f}",
            "tax": f"{tax:.2f}",
            "total": f"{total:.2f}",
        },
    )


def customers_page(request):
    """Customers registration/login page"""
    try:
        r = requests.get(f"{CUSTOMER_SERVICE_URL}/customers/")
        customers = r.json() if r.status_code == 200 else []
    except:
        customers = []
    return render(request, "customers.html", {"customers": customers})


def orders_page(request):
    """Orders list page"""
    customer_id = request.GET.get("customer_id")
    try:
        if customer_id:
            r = requests.get(f"{ORDER_SERVICE_URL}/orders/customer/{customer_id}/")
        else:
            r = requests.get(f"{ORDER_SERVICE_URL}/orders/")
        orders = r.json() if r.status_code == 200 else []
    except:
        orders = []
    return render(request, "orders.html", {"orders": orders})


def catalog_page(request):
    """Catalog page with categories"""
    try:
        r = requests.get(f"{CATALOG_SERVICE_URL}/catalog/")
        catalog = r.json() if r.status_code == 200 else []
    except:
        catalog = []
    return render(request, "catalog.html", {"catalog": catalog})


def staff_page(request):
    """Staff login and book management page"""
    try:
        r = requests.get(f"{BOOK_SERVICE_URL}/books/")
        books = r.json() if r.status_code == 200 else []
    except:
        books = []
    return render(request, "staff.html", {"books": books})


# API Gateway endpoints
def proxy_request(service_url, path, request):
    """Generic proxy function to forward requests to microservices"""
    url = f"{service_url}/{path}"
    try:
        if request.method == "GET":
            r = requests.get(url)
        elif request.method == "POST":
            data = json.loads(request.body) if request.body else {}
            r = requests.post(url, json=data)
        elif request.method == "PUT":
            data = json.loads(request.body) if request.body else {}
            r = requests.put(url, json=data)
        elif request.method == "DELETE":
            r = requests.delete(url)
        else:
            return JsonResponse({"error": "Method not allowed"}, status=405)
        return JsonResponse(r.json(), safe=False, status=r.status_code)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)


