from django.urls import path
from app.views import (
    RecommendForCustomer,
    RecommendSimilarBooks,
    PopularBooks,
    TrendingBooks,
    api_index,
)

urlpatterns = [
    path("", api_index),
    path("recommendations/customer/<int:customer_id>/", RecommendForCustomer.as_view()),
    path("recommendations/similar/<int:book_id>/", RecommendSimilarBooks.as_view()),
    path("recommendations/popular/", PopularBooks.as_view()),
    path("recommendations/trending/", TrendingBooks.as_view()),
]
