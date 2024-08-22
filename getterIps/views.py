from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .utils import fetch_tor_ips, save_ips_to_file, update_last_update_time, get_last_update_time, read_ips_from_file
from .ip_manager import IPManager
from .models import ExcludedIP
from .serializer import ExcludedIPSerializer

import time 

# Documentación de investigación Django IP's: https://docs.djangoproject.com/es/5.1/ref/validators/
"""Dato Random: Al principio perdí mucho tiempo usando diversos, headers y proxies para intentar bypassear el trafico,
   pero la misma pagina me dice que cada 15 min puedo volver a obtener la lista así que no hay problema, cada 15 actualizo"""

# Vista para obtener todas las IP's obtenidas de la fuente externa :) 
@api_view(['GET'])
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
def exclude_ip_view(request):
    return IPManager.exclude_tor_ips(request)

# Vista para obtener las IP's excepto las que están en la BD. 
@api_view(['GET'])
def tor_ips_filtered_view(request):
    try:
        filtered_ips = IPManager.tor_ips_filtered()
        return Response(filtered_ips, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# Vista para poder obtener una IP especifica del conjunto de IPS Excluidas. 
@api_view(['GET'])
def ip_excluded_details_view(request, ip_address):
    try:
        ip = ExcludedIP.objects.get(ip_address=ip_address)
        serializer = ExcludedIPSerializer(ip)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except ExcludedIP.DoesNotExist:
        return Response({'error': 'IP not found'}, status=status.HTTP_404_NOT_FOUND)
    
# Vista para poder eliminar una IP especifica del conjunto de IPS Excluidas. 
@api_view(['DELETE'])
def delete_ip_excluded_view(request, ip_address):
    try:
        ip = ExcludedIP.objects.get(ip_address=ip_address)
        ip.delete()
        return Response({'message': 'IP successfully deleted'}, status=status.HTTP_204_NO_CONTENT)
    except ExcludedIP.DoesNotExist:
        return Response({'error': 'IP not found'}, status=status.HTTP_404_NOT_FOUND)
    
# Vista para obtener todas las IP's Excluidas que se supone están en la Base de datos :) Obvio jaja
@api_view(['GET'])
def excluded_ips_list_view(request):
    """Vista que devuelve una lista de todas las IPs excluidas."""
    excluded_ips = ExcludedIP.objects.all()
    serializer = ExcludedIPSerializer(excluded_ips, many=True)
    return Response(serializer.data)