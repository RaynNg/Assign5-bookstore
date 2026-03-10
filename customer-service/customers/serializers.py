from rest_framework import serializers
from .models import Customer


class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = "__all__"
        extra_kwargs = {"password": {"write_only": True}}


class CustomerRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ["username", "email", "password", "first_name", "last_name", "phone", "address"]
        extra_kwargs = {"password": {"write_only": True}}
