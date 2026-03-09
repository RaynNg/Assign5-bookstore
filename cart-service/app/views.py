from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from .models import Cart, CartItem
from .serializers import CartSerializer, CartItemSerializer
import requests

BOOK_SERVICE_URL = "http://book-service:8000"


@api_view(["GET"])
def api_index(request):
    """API Index - List all available endpoints"""
    return Response(
        {
            "service": "Cart Service",
            "version": "1.0",
            "endpoints": {
                "POST /carts/": "Create cart for customer",
                "GET /carts/<id>/": "Get cart details",
                "GET /carts/customer/<customer_id>/": "Get cart by customer",
                "POST /cart-items/": "Add item to cart",
                "PUT /cart-items/<id>/": "Update cart item",
                "DELETE /cart-items/<id>/": "Remove cart item",
                "GET /carts/<customer_id>/items/": "View cart items",
                "DELETE /carts/<customer_id>/clear/": "Clear cart",
            },
        }
    )


class CartCreate(APIView):
    def post(self, request):
        serializer = CartSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CartDetail(APIView):
    def get(self, request, pk):
        try:
            cart = Cart.objects.get(pk=pk)
            serializer = CartSerializer(cart)
            return Response(serializer.data)
        except Cart.DoesNotExist:
            return Response(
                {"error": "Cart not found"}, status=status.HTTP_404_NOT_FOUND
            )


class CartByCustomer(APIView):
    def get(self, request, customer_id):
        try:
            cart = Cart.objects.get(customer_id=customer_id)
            serializer = CartSerializer(cart)
            return Response(serializer.data)
        except Cart.DoesNotExist:
            return Response(
                {"error": "Cart not found"}, status=status.HTTP_404_NOT_FOUND
            )


class AddCartItem(APIView):
    def post(self, request):
        book_id = request.data.get("book_id")
        try:
            r = requests.get(f"{BOOK_SERVICE_URL}/books/{book_id}/")
            if r.status_code != 200:
                return Response(
                    {"error": "Book not found"}, status=status.HTTP_404_NOT_FOUND
                )
        except:
            pass  # Continue if book service unavailable
        serializer = CartItemSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UpdateCartItem(APIView):
    def put(self, request, pk):
        try:
            item = CartItem.objects.get(pk=pk)
            serializer = CartItemSerializer(item, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except CartItem.DoesNotExist:
            return Response(
                {"error": "Cart item not found"}, status=status.HTTP_404_NOT_FOUND
            )

    def delete(self, request, pk):
        try:
            item = CartItem.objects.get(pk=pk)
            item.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except CartItem.DoesNotExist:
            return Response(
                {"error": "Cart item not found"}, status=status.HTTP_404_NOT_FOUND
            )


class ViewCartItems(APIView):
    def get(self, request, customer_id):
        try:
            cart = Cart.objects.get(customer_id=customer_id)
            items = CartItem.objects.filter(cart=cart)
            serializer = CartItemSerializer(items, many=True)
            return Response(serializer.data)
        except Cart.DoesNotExist:
            return Response(
                {"error": "Cart not found"}, status=status.HTTP_404_NOT_FOUND
            )


class ClearCart(APIView):
    def delete(self, request, customer_id):
        try:
            cart = Cart.objects.get(customer_id=customer_id)
            CartItem.objects.filter(cart=cart).delete()
            return Response({"message": "Cart cleared"})
        except Cart.DoesNotExist:
            return Response(
                {"error": "Cart not found"}, status=status.HTTP_404_NOT_FOUND
            )
