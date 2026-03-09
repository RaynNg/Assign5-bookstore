from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from .models import Category
from .serializers import CategorySerializer
import requests

BOOK_SERVICE_URL = "http://book-service:8000"


@api_view(["GET"])
def api_index(request):
    """API Index - List all available endpoints"""
    return Response(
        {
            "service": "Catalog Service",
            "version": "1.0",
            "endpoints": {
                "GET /categories/": "List all categories",
                "POST /categories/": "Create new category",
                "GET /categories/<id>/": "Get category details",
                "PUT /categories/<id>/": "Update category",
                "DELETE /categories/<id>/": "Delete category",
                "GET /catalog/": "View full catalog with books",
            },
        }
    )


class CategoryListCreate(APIView):
    def get(self, request):
        categories = Category.objects.all()
        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = CategorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CategoryDetail(APIView):
    def get(self, request, pk):
        try:
            category = Category.objects.get(pk=pk)
            serializer = CategorySerializer(category)
            return Response(serializer.data)
        except Category.DoesNotExist:
            return Response(
                {"error": "Category not found"}, status=status.HTTP_404_NOT_FOUND
            )

    def put(self, request, pk):
        try:
            category = Category.objects.get(pk=pk)
            serializer = CategorySerializer(category, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Category.DoesNotExist:
            return Response(
                {"error": "Category not found"}, status=status.HTTP_404_NOT_FOUND
            )

    def delete(self, request, pk):
        try:
            category = Category.objects.get(pk=pk)
            category.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Category.DoesNotExist:
            return Response(
                {"error": "Category not found"}, status=status.HTTP_404_NOT_FOUND
            )


class CatalogView(APIView):
    """View full catalog with categories and books"""

    def get(self, request):
        try:
            # Get all categories
            categories = Category.objects.all()
            categories_data = CategorySerializer(categories, many=True).data

            # Get all books from book-service
            try:
                books_response = requests.get(f"{BOOK_SERVICE_URL}/books/")
                books = (
                    books_response.json() if books_response.status_code == 200 else []
                )
            except requests.RequestException:
                books = []

            return Response({"categories": categories_data, "books": books})
        except Exception as e:
            return Response(
                {"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
