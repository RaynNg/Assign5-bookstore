from django.urls import path
from app.views import (
    CartCreate,
    CartDetail,
    CartByCustomer,
    AddCartItem,
    UpdateCartItem,
    ViewCartItems,
    ClearCart,
    api_index,
)

urlpatterns = [
    path("", api_index),
    path("carts/", CartCreate.as_view()),
    path("carts/<int:pk>/", CartDetail.as_view()),
    path("carts/customer/<int:customer_id>/", CartByCustomer.as_view()),
    path("cart-items/", AddCartItem.as_view()),
    path("cart-items/<int:pk>/", UpdateCartItem.as_view()),
    path("carts/<int:customer_id>/items/", ViewCartItems.as_view()),
    path("carts/<int:customer_id>/clear/", ClearCart.as_view()),
]
