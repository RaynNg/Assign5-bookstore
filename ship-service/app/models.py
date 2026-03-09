from django.db import models


class Shipment(models.Model):
    STATUS_CHOICES = [
        ("pending", "Pending"),
        ("processing", "Processing"),
        ("shipped", "Shipped"),
        ("in_transit", "In Transit"),
        ("delivered", "Delivered"),
        ("failed", "Failed"),
    ]

    METHOD_CHOICES = [
        ("standard", "Standard Shipping"),
        ("express", "Express Shipping"),
        ("overnight", "Overnight Shipping"),
    ]

    order_id = models.IntegerField()
    method = models.CharField(max_length=50, choices=METHOD_CHOICES, default="standard")
    address = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="pending")
    tracking_number = models.CharField(max_length=100, blank=True)
    estimated_delivery = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Shipment #{self.id} - Order {self.order_id}"
