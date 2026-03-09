from django.urls import path
from app.views import (
    OrderListCreate,
    OrderDetail,
    CreateOrderFromCart,
    CustomerOrders,
    api_index,
)

urlpatterns = [
    path("", api_index),
    path("orders/", OrderListCreate.as_view()),
    path("orders/<int:pk>/", OrderDetail.as_view()),
    path("orders/checkout/", CreateOrderFromCart.as_view()),
    path("orders/customer/<int:customer_id>/", CustomerOrders.as_view()),
]
