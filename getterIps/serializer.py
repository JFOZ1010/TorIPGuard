import ipaddress
from rest_framework import serializers
from .models import ExcludedIP

class ExcludedIPSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExcludedIP
        fields = ['ip_address', 'created_at']
        #fields = '__all__'

    def validate_ip_address(self, value):
        # Validar si la IP es válida (IPv4 o IPv6) usando la librería `ipaddress`
        try:
            ip = ipaddress.ip_address(value)
            print(f"Valid IP address: {ip}")
        except ValueError:
            raise serializers.ValidationError("Invalid IP address")
        return value
