from rest_framework import serializers
from .models import ExcludedIP

class ExcludedIPSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExcludedIP
        fields = ['ip_address']

    def validate_ip_address(self, value):
        # Validar si la IP es válida (IPv4 o IPv6)
        try:
            serializers.validate_ipv4_address(value)
        except serializers.ValidationError:
            try:
                serializers.validate_ipv6_address(value)
            except serializers.ValidationError:
                raise serializers.ValidationError("Invalid IP address")
        return value
