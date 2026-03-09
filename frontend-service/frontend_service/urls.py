from django.urls import path
from . import views

urlpatterns = [
    # HTML Views
    path("", views.home, name="home"),
    path("books/", views.book_list, name="books"),
    path("cart/", views.view_cart, name="cart_empty"),
    path("cart/<int:customer_id>/", views.view_cart, name="cart"),
    path("customers/", views.customers_page, name="customers"),
    path("orders/", views.orders_page, name="orders"),
    path("catalog/", views.catalog_page, name="catalog"),
    path("staff/", views.staff_page, name="staff"),
]
