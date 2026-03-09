from rest_framework import serializers
from .models import Staff


class StaffSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = Staff
        fields = ["id", "name", "email", "password", "role", "created_at"]
        read_only_fields = ["id", "created_at"]

    def create(self, validated_data):
        password = validated_data.pop("password")
        staff = Staff(**validated_data)
        staff.set_password(password)
        staff.save()
        return staff


class StaffLoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()
