import json
from django.core.exceptions import ValidationError
from django.core.validators import validate_ipv4_address, validate_ipv6_address
from rest_framework.response import Response
from rest_framework import status
from .models import ExcludedIP
from .utils import read_ips_from_file

class IPManager:
    @staticmethod
    def exclude_tor_ips(request):
        try:
            data = json.loads(request.body)
            ip = data.get('ip')

            if not ip:
                return Response({'error': 'IP is required'}, status=status.HTTP_400_BAD_REQUEST)

            # Validar IP
            try:
                validate_ipv4_address(ip)
            except ValidationError:
                try:
                    validate_ipv6_address(ip)
                except ValidationError:
                    return Response({'error': 'Invalid IP address'}, status=status.HTTP_400_BAD_REQUEST)

            # Guardar en base de datos
            ExcludedIP.objects.get_or_create(ip_address=ip)

            # Guardar la IP en el archivo
            with open('ips-tor2.txt', 'a') as file:
                file.write(f"{ip}\n")

            return Response({'message': 'IP added successfully'}, status=status.HTTP_200_OK)
        except json.JSONDecodeError:
            return Response({'error': 'Invalid JSON'}, status=status.HTTP_400_BAD_REQUEST)

    @staticmethod
    def tor_ips_filtered():
        """Filtra las IPs de TOR excluyendo las IPs de la base de datos."""
        all_ips = read_ips_from_file()
        excluded_ips = ExcludedIP.objects.values_list('ip_address', flat=True)
        excluded_ips_set = set(excluded_ips)

        all_ips_set = set(all_ips)
        filtered_ips = all_ips_set - excluded_ips_set
        return list(filtered_ips)
