from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from .models import Staff
from .serializers import StaffSerializer, StaffLoginSerializer
import requests

BOOK_SERVICE_URL = "http://book-service:8000"


@api_view(["GET"])
def api_index(request):
    """API Index - List all available endpoints"""
    return Response(
        {
            "service": "Staff Service",
            "version": "1.0",
            "description": "Staff manages books",
            "endpoints": {
                "GET /staff/": "List all staff",
                "POST /staff/": "Create/Register new staff",
                "POST /staff/login/": "Staff login",
                "GET /staff/<id>/": "Get staff details",
                "PUT /staff/<id>/": "Update staff",
                "DELETE /staff/<id>/": "Delete staff",
                "POST /staff/manage-book/": "Create book (staff action)",
                "PUT /staff/manage-book/<book_id>/": "Update book (staff action)",
                "DELETE /staff/manage-book/<book_id>/": "Delete book (staff action)",
            },
        }
    )


class StaffLogin(APIView):
    """Staff login endpoint"""

    def post(self, request):
        serializer = StaffLoginSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data["email"]
            password = serializer.validated_data["password"]

            try:
                staff = Staff.objects.get(email=email)
                if staff.check_password(password):
                    return Response(
                        {
                            "message": "Login successful",
                            "staff": {
                                "id": staff.id,
                                "name": staff.name,
                                "email": staff.email,
                                "role": staff.role,
                            },
                        }
                    )
                else:
                    return Response(
                        {"error": "Invalid password"},
                        status=status.HTTP_401_UNAUTHORIZED,
                    )
            except Staff.DoesNotExist:
                return Response(
                    {"error": "Staff not found"}, status=status.HTTP_404_NOT_FOUND
                )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class StaffListCreate(APIView):
    def get(self, request):
        staff = Staff.objects.all()
        serializer = StaffSerializer(staff, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = StaffSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class StaffDetail(APIView):
    def get(self, request, pk):
        try:
            staff = Staff.objects.get(pk=pk)
            serializer = StaffSerializer(staff)
            return Response(serializer.data)
        except Staff.DoesNotExist:
            return Response(
                {"error": "Staff not found"}, status=status.HTTP_404_NOT_FOUND
            )

    def put(self, request, pk):
        try:
            staff = Staff.objects.get(pk=pk)
            serializer = StaffSerializer(staff, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Staff.DoesNotExist:
            return Response(
                {"error": "Staff not found"}, status=status.HTTP_404_NOT_FOUND
            )

    def delete(self, request, pk):
        try:
            staff = Staff.objects.get(pk=pk)
            staff.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Staff.DoesNotExist:
            return Response(
                {"error": "Staff not found"}, status=status.HTTP_404_NOT_FOUND
            )


class ManageBook(APIView):
    """Staff can manage books - CRUD operations"""

    def post(self, request):
        """Create a new book"""
        try:
            response = requests.post(f"{BOOK_SERVICE_URL}/books/", json=request.data)
            return Response(response.json(), status=response.status_code)
        except requests.RequestException as e:
            return Response(
                {"error": str(e)}, status=status.HTTP_503_SERVICE_UNAVAILABLE
            )

    def put(self, request, book_id):
        """Update a book"""
        try:
            response = requests.put(
                f"{BOOK_SERVICE_URL}/books/{book_id}/", json=request.data
            )
            return Response(response.json(), status=response.status_code)
        except requests.RequestException as e:
            return Response(
                {"error": str(e)}, status=status.HTTP_503_SERVICE_UNAVAILABLE
            )

    def delete(self, request, book_id):
        """Delete a book"""
        try:
            response = requests.delete(f"{BOOK_SERVICE_URL}/books/{book_id}/")
            return Response(status=response.status_code)
        except requests.RequestException as e:
            return Response(
                {"error": str(e)}, status=status.HTTP_503_SERVICE_UNAVAILABLE
            )
