from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CatalogViewSet

router = DefaultRouter()
router.register(r"catalogs", CatalogViewSet)

urlpatterns = [
    path("", include(router.urls)),
]
