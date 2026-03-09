from django.urls import path
from app.views import CategoryListCreate, CategoryDetail, CatalogView, api_index

urlpatterns = [
    path("", api_index),
    path("categories/", CategoryListCreate.as_view()),
    path("categories/<int:pk>/", CategoryDetail.as_view()),
    path("catalog/", CatalogView.as_view()),
]
