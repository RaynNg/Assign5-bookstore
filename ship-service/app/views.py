from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from .models import Shipment
from .serializers import ShipmentSerializer
import uuid
from datetime import datetime, timedelta


@api_view(["GET"])
def api_index(request):
    """API Index - List all available endpoints"""
    return Response(
        {
            "service": "Shipping Service",
            "version": "1.0",
            "endpoints": {
                "GET /shipments/": "List all shipments",
                "POST /shipments/": "Create shipment (customer selects method)",
                "GET /shipments/<id>/": "Get shipment details",
                "PUT /shipments/<id>/": "Update shipment",
                "PUT /shipments/<id>/status/": "Update shipment status",
                "GET /shipping-methods/": "List available shipping methods",
            },
        }
    )


class ShipmentListCreate(APIView):
    def get(self, request):
        shipments = Shipment.objects.all()
        serializer = ShipmentSerializer(shipments, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = ShipmentSerializer(data=request.data)
        if serializer.is_valid():
            shipment = serializer.save()

            # Generate tracking number
            shipment.tracking_number = f"TRK{uuid.uuid4().hex[:10].upper()}"

            # Set estimated delivery based on method
            if shipment.method == "overnight":
                shipment.estimated_delivery = datetime.now().date() + timedelta(days=1)
            elif shipment.method == "express":
                shipment.estimated_delivery = datetime.now().date() + timedelta(days=3)
            else:
                shipment.estimated_delivery = datetime.now().date() + timedelta(days=7)

            shipment.status = "processing"
            shipment.save()

            return Response(
                ShipmentSerializer(shipment).data, status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ShipmentDetail(APIView):
    def get(self, request, pk):
        try:
            shipment = Shipment.objects.get(pk=pk)
            serializer = ShipmentSerializer(shipment)
            return Response(serializer.data)
        except Shipment.DoesNotExist:
            return Response(
                {"error": "Shipment not found"}, status=status.HTTP_404_NOT_FOUND
            )

    def put(self, request, pk):
        try:
            shipment = Shipment.objects.get(pk=pk)
            serializer = ShipmentSerializer(shipment, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Shipment.DoesNotExist:
            return Response(
                {"error": "Shipment not found"}, status=status.HTTP_404_NOT_FOUND
            )

    def delete(self, request, pk):
        try:
            shipment = Shipment.objects.get(pk=pk)
            shipment.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Shipment.DoesNotExist:
            return Response(
                {"error": "Shipment not found"}, status=status.HTTP_404_NOT_FOUND
            )


class UpdateShipmentStatus(APIView):
    """Update shipment status"""

    def put(self, request, pk):
        try:
            shipment = Shipment.objects.get(pk=pk)
            new_status = request.data.get("status")

            valid_statuses = [
                "pending",
                "processing",
                "shipped",
                "in_transit",
                "delivered",
                "failed",
            ]
            if new_status not in valid_statuses:
                return Response(
                    {"error": f"Invalid status. Valid options: {valid_statuses}"},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            shipment.status = new_status
            shipment.save()

            serializer = ShipmentSerializer(shipment)
            return Response(serializer.data)
        except Shipment.DoesNotExist:
            return Response(
                {"error": "Shipment not found"}, status=status.HTTP_404_NOT_FOUND
            )


class ShippingMethods(APIView):
    """Get available shipping methods"""

    def get(self, request):
        methods = [
            {
                "id": "standard",
                "name": "Standard Shipping",
                "price": 5.99,
                "days": "5-7 business days",
            },
            {
                "id": "express",
                "name": "Express Shipping",
                "price": 12.99,
                "days": "2-3 business days",
            },
            {
                "id": "overnight",
                "name": "Overnight Shipping",
                "price": 24.99,
                "days": "1 business day",
            },
        ]
        return Response(methods)
