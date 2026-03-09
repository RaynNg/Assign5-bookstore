from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from .models import Payment
from .serializers import PaymentSerializer
import uuid


@api_view(["GET"])
def api_index(request):
    """API Index - List all available endpoints"""
    return Response(
        {
            "service": "Payment Service",
            "version": "1.0",
            "endpoints": {
                "GET /payments/": "List all payments",
                "POST /payments/": "Process payment (customer selects method)",
                "GET /payments/<id>/": "Get payment details",
                "PUT /payments/<id>/": "Update payment status",
                "POST /payments/<id>/refund/": "Process refund",
                "GET /payment-methods/": "List available payment methods",
            },
        }
    )


class PaymentListCreate(APIView):
    def get(self, request):
        payments = Payment.objects.all()
        serializer = PaymentSerializer(payments, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = PaymentSerializer(data=request.data)
        if serializer.is_valid():
            payment = serializer.save()

            # Simulate payment processing
            payment.transaction_id = f"TXN{uuid.uuid4().hex[:12].upper()}"
            payment.status = (
                "completed"  # In real scenario, this would depend on payment gateway
            )
            payment.save()

            return Response(
                PaymentSerializer(payment).data, status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PaymentDetail(APIView):
    def get(self, request, pk):
        try:
            payment = Payment.objects.get(pk=pk)
            serializer = PaymentSerializer(payment)
            return Response(serializer.data)
        except Payment.DoesNotExist:
            return Response(
                {"error": "Payment not found"}, status=status.HTTP_404_NOT_FOUND
            )

    def put(self, request, pk):
        try:
            payment = Payment.objects.get(pk=pk)
            serializer = PaymentSerializer(payment, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Payment.DoesNotExist:
            return Response(
                {"error": "Payment not found"}, status=status.HTTP_404_NOT_FOUND
            )

    def delete(self, request, pk):
        try:
            payment = Payment.objects.get(pk=pk)
            payment.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Payment.DoesNotExist:
            return Response(
                {"error": "Payment not found"}, status=status.HTTP_404_NOT_FOUND
            )


class ProcessRefund(APIView):
    """Process refund for a payment"""

    def post(self, request, pk):
        try:
            payment = Payment.objects.get(pk=pk)

            if payment.status != "completed":
                return Response(
                    {"error": "Can only refund completed payments"},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            # Simulate refund processing
            payment.status = "refunded"
            payment.save()

            serializer = PaymentSerializer(payment)
            return Response(
                {"message": "Refund processed successfully", "payment": serializer.data}
            )
        except Payment.DoesNotExist:
            return Response(
                {"error": "Payment not found"}, status=status.HTTP_404_NOT_FOUND
            )


class PaymentMethods(APIView):
    """Get available payment methods"""

    def get(self, request):
        methods = [
            {"id": "credit_card", "name": "Credit Card", "icon": "💳"},
            {"id": "debit_card", "name": "Debit Card", "icon": "💳"},
            {"id": "paypal", "name": "PayPal", "icon": "🅿️"},
            {"id": "bank_transfer", "name": "Bank Transfer", "icon": "🏦"},
            {"id": "cash_on_delivery", "name": "Cash on Delivery", "icon": "💵"},
        ]
        return Response(methods)
