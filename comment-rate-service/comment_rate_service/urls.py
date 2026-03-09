from django.urls import path
from app.views import (
    ReviewListCreate,
    ReviewDetail,
    BookReviews,
    BookAverageRating,
    api_index,
)

urlpatterns = [
    path("", api_index),
    path("reviews/", ReviewListCreate.as_view()),
    path("reviews/<int:pk>/", ReviewDetail.as_view()),
    path("reviews/book/<int:book_id>/", BookReviews.as_view()),
    path("reviews/book/<int:book_id>/rating/", BookAverageRating.as_view()),
]
