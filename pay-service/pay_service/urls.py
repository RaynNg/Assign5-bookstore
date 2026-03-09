from django.urls import path
from app.views import (
    PaymentListCreate,
    PaymentDetail,
    PaymentMethods,
    ProcessRefund,
    api_index,
)

urlpatterns = [
    path("", api_index),
    path("payments/", PaymentListCreate.as_view()),
    path("payments/<int:pk>/", PaymentDetail.as_view()),
    path("payments/<int:pk>/refund/", ProcessRefund.as_view()),
    path("payment-methods/", PaymentMethods.as_view()),
]
