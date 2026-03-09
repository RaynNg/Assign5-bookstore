from django.urls import path
from app.views import (
    ShipmentListCreate,
    ShipmentDetail,
    ShippingMethods,
    UpdateShipmentStatus,
    api_index,
)

urlpatterns = [
    path("", api_index),
    path("shipments/", ShipmentListCreate.as_view()),
    path("shipments/<int:pk>/", ShipmentDetail.as_view()),
    path("shipments/<int:pk>/status/", UpdateShipmentStatus.as_view()),
    path("shipping-methods/", ShippingMethods.as_view()),
]
