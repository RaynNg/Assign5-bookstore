from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from .models import Manager
from .serializers import ManagerSerializer
import requests

STAFF_SERVICE_URL = "http://staff-service:8000"
ORDER_SERVICE_URL = "http://order-service:8000"


@api_view(["GET"])
def api_index(request):
    """API Index - List all available endpoints"""
    return Response(
        {
            "service": "Manager Service",
            "version": "1.0",
            "endpoints": {
                "GET /managers/": "List all managers",
                "POST /managers/": "Create new manager",
                "GET /managers/<id>/": "Get manager details",
                "PUT /managers/<id>/": "Update manager",
                "DELETE /managers/<id>/": "Delete manager",
                "GET /managers/staff/": "View all staff",
                "GET /managers/reports/": "View sales reports",
            },
        }
    )


class ManagerListCreate(APIView):
    def get(self, request):
        managers = Manager.objects.all()
        serializer = ManagerSerializer(managers, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = ManagerSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ManagerDetail(APIView):
    def get(self, request, pk):
        try:
            manager = Manager.objects.get(pk=pk)
            serializer = ManagerSerializer(manager)
            return Response(serializer.data)
        except Manager.DoesNotExist:
            return Response(
                {"error": "Manager not found"}, status=status.HTTP_404_NOT_FOUND
            )

    def put(self, request, pk):
        try:
            manager = Manager.objects.get(pk=pk)
            serializer = ManagerSerializer(manager, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Manager.DoesNotExist:
            return Response(
                {"error": "Manager not found"}, status=status.HTTP_404_NOT_FOUND
            )

    def delete(self, request, pk):
        try:
            manager = Manager.objects.get(pk=pk)
            manager.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Manager.DoesNotExist:
            return Response(
                {"error": "Manager not found"}, status=status.HTTP_404_NOT_FOUND
            )


class StaffManagement(APIView):
    """Manager can manage staff"""

    def get(self, request):
        """Get all staff"""
        try:
            response = requests.get(f"{STAFF_SERVICE_URL}/staff/")
            return Response(response.json(), status=response.status_code)
        except requests.RequestException as e:
            return Response(
                {"error": str(e)}, status=status.HTTP_503_SERVICE_UNAVAILABLE
            )

    def post(self, request):
        """Create new staff"""
        try:
            response = requests.post(f"{STAFF_SERVICE_URL}/staff/", json=request.data)
            return Response(response.json(), status=response.status_code)
        except requests.RequestException as e:
            return Response(
                {"error": str(e)}, status=status.HTTP_503_SERVICE_UNAVAILABLE
            )


class ReportView(APIView):
    """Manager can view reports"""

    def get(self, request):
        """Get sales reports"""
        try:
            orders_response = requests.get(f"{ORDER_SERVICE_URL}/orders/")
            orders = (
                orders_response.json() if orders_response.status_code == 200 else []
            )

            total_orders = len(orders)
            total_revenue = sum(order.get("total_amount", 0) for order in orders)

            return Response(
                {
                    "total_orders": total_orders,
                    "total_revenue": total_revenue,
                    "orders": orders,
                }
            )
        except requests.RequestException as e:
            return Response(
                {"error": str(e)}, status=status.HTTP_503_SERVICE_UNAVAILABLE
            )
