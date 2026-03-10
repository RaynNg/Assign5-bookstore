from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CommentRateViewSet

router = DefaultRouter()
router.register(r"comments", CommentRateViewSet)

urlpatterns = [
    path("", include(router.urls)),
]
