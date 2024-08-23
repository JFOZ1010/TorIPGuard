from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from django.core.validators import validate_ipv4_address, validate_ipv6_address
from django.core.exceptions import ValidationError
from .utils import fetch_tor_ips, save_ips_to_file, update_last_update_time, get_last_update_time, read_ips_from_file #todas mis funciones necesarias. 
from .ip_manager import IPManager
from .models import ExcludedIP

import time 

# Documentación de investigación Django IP's: https://docs.djangoproject.com/es/5.1/ref/validators/
"""Dato Random: Al principio perdí mucho tiempo usando diversos, headers y proxies para intentar bypassear el trafico,
   pero la misma pagina me dice que cada 15 min puedo volver a obtener la lista así que no hay problema, cada 15 actualizo"""

# Vista para obtener todas las IP's obtenidas de la fuente externa :) 
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def tor_ips_view(request):
    current_time = time.time()
    last_update_time = get_last_update_time()

    # Actualiza las IPs si han pasado más de 15 minutos
    if current_time - last_update_time > 15 * 60:
        ips = fetch_tor_ips()
        save_ips_to_file(ips, filename='ips-tor1.txt')
        update_last_update_time()

    # Lee las IPs del archivo y devuelve la respuesta JSON
    ips_from_file = read_ips_from_file(filename='ips-tor1.txt')
    return Response({'ips': ips_from_file}, status=status.HTTP_200_OK)

# Vista para enviar una IP a la BD y excluirla de las demás (Para una blacklist)
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def exclude_ip_view(request):
    return IPManager.exclude_tor_ips(request)

# Vista para obtener las IP's excepto las que están en la BD. 
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def tor_ips_filtered_view(request):
    try:
        filtered_ips = IPManager.tor_ips_filtered()
        return Response(filtered_ips, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
# Vista que devuelve el conteo total de IPs excluidas.
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def count_excluded_ips_view(request):
    count = ExcludedIP.objects.count()
    return Response({'count': count}, status=status.HTTP_200_OK)

# Vista que devuelve estadísticas sobre las IPs excluidas. (Totas excluidas, ultima ip, ultima ip creada)
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def ip_stats_view(request):
    total_excluded = ExcludedIP.objects.count()
    latest_ip = ExcludedIP.objects.latest('created_at') if total_excluded > 0 else None
    stats = {
        'total_excluded': total_excluded,
        'latest_ip': latest_ip.ip_address if latest_ip else None,
        'latest_ip_created_at': latest_ip.created_at if latest_ip else None,
    }
    return Response(stats, status=status.HTTP_200_OK)

# Vista que devuelve el conteo total de todas las IPs del archivo ips-tor1.txt que es el que guarda todas las nuevas IPS obtenidas de la fuente externa.
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def count_all_ips_view(request):
    ips = read_ips_from_file()
    count = len(ips)
    return Response({'count': count}, status=status.HTTP_200_OK)

# Vista que actualiza una IP excluida en la base de datos.
@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_excluded_ip_view(request):
    data = request.data
    old_ip = data.get('old_ip')
    new_ip = data.get('new_ip')

    if not old_ip or not new_ip:
        return Response({'error': 'Both old_ip and new_ip are required'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        validate_ipv4_address(new_ip)
    except ValidationError:
        try:
            validate_ipv6_address(new_ip)
        except ValidationError:
            return Response({'error': 'Invalid new IP address'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        ip_entry = ExcludedIP.objects.get(ip_address=old_ip)
        ip_entry.ip_address = new_ip
        ip_entry.save()
        return Response({'message': 'IP updated successfully'}, status=status.HTTP_200_OK)
    except ExcludedIP.DoesNotExist:
        return Response({'error': 'Old IP not found'}, status=status.HTTP_404_NOT_FOUND)
    
# Vista para eliminar una IP específica de las excluidas xd
@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_specific_excluded_ip_view(request, ip_address):
    
    try:
        ip = ExcludedIP.objects.get(ip_address=ip_address)
        ip.delete()
        return Response({'message': 'IP successfully deleted'}, status=status.HTTP_204_NO_CONTENT)
    except ExcludedIP.DoesNotExist:
        return Response({'error': 'IP not found'}, status=status.HTTP_404_NOT_FOUND)
    


    
""" # Vista para obtener todas las IPs excluidas :) 
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def list_all_excluded_ips_post_view(request):
    excluded_ips = ExcludedIP.objects.all()
    serializer = ExcludedIPSerializer(excluded_ips, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK) """