from django.urls import path
from app.views import CustomerListCreate, CustomerDetail, CustomerLogin, api_index

urlpatterns = [
    path("", api_index),
    path("customers/", CustomerListCreate.as_view()),
    path("customers/login/", CustomerLogin.as_view()),
    path("customers/<int:pk>/", CustomerDetail.as_view()),
]
