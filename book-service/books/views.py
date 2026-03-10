import os
import requests
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Book
from .serializers import BookSerializer

STAFF_SERVICE_URL = os.environ.get("STAFF_SERVICE_URL", "http://staff-service:8000")
CATALOG_SERVICE_URL = os.environ.get("CATALOG_SERVICE_URL", "http://catalog-service:8000")


class BookViewSet(viewsets.ModelViewSet):
    """Staff manages books (CRUD). All users can list/retrieve."""
    queryset = Book.objects.all()
    serializer_class = BookSerializer

    @action(detail=False, methods=["get"])
    def by_catalog(self, request):
        catalog_id = request.query_params.get("catalog_id")
        if not catalog_id:
            return Response({"error": "catalog_id is required"}, status=status.HTTP_400_BAD_REQUEST)
        books = Book.objects.filter(catalog_id=catalog_id)
        serializer = self.get_serializer(books, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=["get"])
    def search(self, request):
        q = request.query_params.get("q", "")
        books = Book.objects.filter(title__icontains=q)
        serializer = self.get_serializer(books, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=["post"])
    def update_stock(self, request, pk=None):
        book = self.get_object()
        quantity = int(request.data.get("quantity", 0))
        book.stock += quantity
        if book.stock < 0:
            return Response({"error": "Insufficient stock"}, status=status.HTTP_400_BAD_REQUEST)
        book.save()
        return Response(BookSerializer(book).data)
