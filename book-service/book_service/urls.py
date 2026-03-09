from django.urls import path
from app.views import BookListCreate, BookDetail, api_index

urlpatterns = [
    path("", api_index),
    path("books/", BookListCreate.as_view()),
    path("books/<int:pk>/", BookDetail.as_view()),
]
