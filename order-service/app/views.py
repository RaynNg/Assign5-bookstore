from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from .models import Order, OrderItem
from .serializers import OrderSerializer, OrderItemSerializer
import requests

CART_SERVICE_URL = "http://cart-service:8000"
BOOK_SERVICE_URL = "http://book-service:8000"
PAY_SERVICE_URL = "http://pay-service:8000"
SHIP_SERVICE_URL = "http://ship-service:8000"


@api_view(["GET"])
def api_index(request):
    """API Index - List all available endpoints"""
    return Response(
        {
            "service": "Order Service",
            "version": "1.0",
            "description": "Order triggers payment and shipping",
            "endpoints": {
                "GET /orders/": "List all orders",
                "POST /orders/": "Create new order",
                "GET /orders/<id>/": "Get order details",
                "PUT /orders/<id>/": "Update order",
                "DELETE /orders/<id>/": "Delete order",
                "POST /orders/checkout/": "Checkout - create order from cart, trigger payment & shipping",
                "GET /orders/customer/<customer_id>/": "Get customer's orders",
            },
        }
    )


class OrderListCreate(APIView):
    def get(self, request):
        orders = Order.objects.all()
        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = OrderSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class OrderDetail(APIView):
    def get(self, request, pk):
        try:
            order = Order.objects.get(pk=pk)
            serializer = OrderSerializer(order)
            return Response(serializer.data)
        except Order.DoesNotExist:
            return Response(
                {"error": "Order not found"}, status=status.HTTP_404_NOT_FOUND
            )

    def put(self, request, pk):
        try:
            order = Order.objects.get(pk=pk)
            serializer = OrderSerializer(order, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Order.DoesNotExist:
            return Response(
                {"error": "Order not found"}, status=status.HTTP_404_NOT_FOUND
            )

    def delete(self, request, pk):
        try:
            order = Order.objects.get(pk=pk)
            order.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Order.DoesNotExist:
            return Response(
                {"error": "Order not found"}, status=status.HTTP_404_NOT_FOUND
            )


class CreateOrderFromCart(APIView):
    """
    Create order from cart, trigger payment and shipping
    Request body:
    {
        "customer_id": 1,
        "payment_method": "credit_card",
        "shipping_method": "express",
        "shipping_address": "123 Main St"
    }
    """

    def post(self, request):
        customer_id = request.data.get("customer_id")
        payment_method = request.data.get("payment_method", "credit_card")
        shipping_method = request.data.get("shipping_method", "standard")
        shipping_address = request.data.get("shipping_address", "")

        if not customer_id:
            return Response(
                {"error": "customer_id is required"}, status=status.HTTP_400_BAD_REQUEST
            )

        try:
            # 1. Get cart items from cart-service
            cart_response = requests.get(f"{CART_SERVICE_URL}/carts/{customer_id}/")
            if cart_response.status_code != 200:
                return Response(
                    {"error": "Failed to get cart"}, status=status.HTTP_400_BAD_REQUEST
                )

            cart_items = cart_response.json()
            if not cart_items:
                return Response(
                    {"error": "Cart is empty"}, status=status.HTTP_400_BAD_REQUEST
                )

            # 2. Get book prices and calculate total
            total_amount = 0
            order_items_data = []

            for item in cart_items:
                book_id = item.get("book_id")
                quantity = item.get("quantity", 1)

                # Get book price from book-service
                try:
                    book_response = requests.get(f"{BOOK_SERVICE_URL}/books/{book_id}/")
                    if book_response.status_code == 200:
                        book = book_response.json()
                        price = float(book.get("price", 0))
                        total_amount += price * quantity
                        order_items_data.append(
                            {"book_id": book_id, "quantity": quantity, "price": price}
                        )
                except requests.RequestException:
                    pass

            # 3. Create order
            order = Order.objects.create(
                customer_id=customer_id,
                total_amount=total_amount,
                payment_method=payment_method,
                shipping_method=shipping_method,
                shipping_address=shipping_address,
                status="pending",
            )

            # 4. Create order items
            for item_data in order_items_data:
                OrderItem.objects.create(
                    order=order,
                    book_id=item_data["book_id"],
                    quantity=item_data["quantity"],
                    price=item_data["price"],
                )

            # 5. Trigger payment service
            try:
                pay_response = requests.post(
                    f"{PAY_SERVICE_URL}/payments/",
                    json={
                        "order_id": order.id,
                        "amount": float(total_amount),
                        "method": payment_method,
                    },
                )
                if pay_response.status_code in [200, 201]:
                    order.status = "paid"
                    order.save()
            except requests.RequestException as e:
                pass  # Payment service unavailable, order remains pending

            # 6. Trigger shipping service
            try:
                ship_response = requests.post(
                    f"{SHIP_SERVICE_URL}/shipments/",
                    json={
                        "order_id": order.id,
                        "method": shipping_method,
                        "address": shipping_address,
                    },
                )
            except requests.RequestException as e:
                pass  # Shipping service unavailable

            # 7. Clear cart after successful order
            try:
                requests.delete(f"{CART_SERVICE_URL}/carts/{customer_id}/clear/")
            except requests.RequestException:
                pass

            serializer = OrderSerializer(order)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response(
                {"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class CustomerOrders(APIView):
    """Get all orders for a specific customer"""

    def get(self, request, customer_id):
        orders = Order.objects.filter(customer_id=customer_id).order_by("-created_at")
        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data)
