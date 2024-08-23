from rest_framework import serializers
from django.core.validators import validate_ipv4_address, validate_ipv6_address
from django.core.exceptions import ValidationError
from .models import ExcludedIP

class ExcludedIPSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExcludedIP
        fields = ['ip_address']

    def validate_ip_address(self, value):
        # Validar si la IP es válida (IPv4 o IPv6)
        try:
            validate_ipv4_address(value)
        except ValidationError:
            try:
                validate_ipv6_address(value)
            except ValidationError:
                raise serializers.ValidationError("Invalid IP address")
        return value