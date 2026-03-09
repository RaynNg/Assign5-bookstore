from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from .models import Customer
from .serializers import CustomerSerializer, CustomerLoginSerializer
import requests

CART_SERVICE_URL = "http://cart-service:8000"


@api_view(["GET"])
def api_index(request):
    """API Index - List all available endpoints"""
    return Response(
        {
            "service": "Customer Service",
            "version": "1.0",
            "endpoints": {
                "GET /customers/": "List all customers",
                "POST /customers/": "Register new customer (auto-creates cart)",
                "POST /customers/login/": "Customer login",
                "GET /customers/<id>/": "Get customer details",
                "PUT /customers/<id>/": "Update customer",
                "DELETE /customers/<id>/": "Delete customer",
            },
        }
    )


class CustomerLogin(APIView):
    """Customer login endpoint"""

    def post(self, request):
        serializer = CustomerLoginSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data["email"]
            password = serializer.validated_data["password"]

            try:
                customer = Customer.objects.get(email=email)
                if customer.check_password(password):
                    return Response(
                        {
                            "message": "Login successful",
                            "customer": {
                                "id": customer.id,
                                "name": customer.name,
                                "email": customer.email,
                            },
                        }
                    )
                else:
                    return Response(
                        {"error": "Invalid password"},
                        status=status.HTTP_401_UNAUTHORIZED,
                    )
            except Customer.DoesNotExist:
                return Response(
                    {"error": "Customer not found"}, status=status.HTTP_404_NOT_FOUND
                )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CustomerListCreate(APIView):
    def get(self, request):
        customers = Customer.objects.all()
        serializer = CustomerSerializer(customers, many=True)
        return Response(serializer.data)

    def post(self, request):
        """Customer registration automatically creates a cart"""
        serializer = CustomerSerializer(data=request.data)
        if serializer.is_valid():
            customer = serializer.save()

            # Call cart-service to create cart for new customer
            try:
                requests.post(
                    f"{CART_SERVICE_URL}/carts/", json={"customer_id": customer.id}
                )
            except requests.RequestException:
                pass  # Cart service unavailable, continue anyway

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CustomerDetail(APIView):
    def get(self, request, pk):
        try:
            customer = Customer.objects.get(pk=pk)
            serializer = CustomerSerializer(customer)
            return Response(serializer.data)
        except Customer.DoesNotExist:
            return Response(
                {"error": "Customer not found"}, status=status.HTTP_404_NOT_FOUND
            )

    def put(self, request, pk):
        try:
            customer = Customer.objects.get(pk=pk)
            serializer = CustomerSerializer(customer, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Customer.DoesNotExist:
            return Response(
                {"error": "Customer not found"}, status=status.HTTP_404_NOT_FOUND
            )

    def delete(self, request, pk):
        try:
            customer = Customer.objects.get(pk=pk)
            customer.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Customer.DoesNotExist:
            return Response(
                {"error": "Customer not found"}, status=status.HTTP_404_NOT_FOUND
            )
