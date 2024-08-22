from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.http import require_GET
from django.views.decorators.csrf import csrf_exempt
from django.core.exceptions import ValidationError
from django.core.validators import validate_ipv4_address, validate_ipv6_address
from bs4 import BeautifulSoup
from lxml import etree
from .models import ExcludedIP #Modelo para excluir IPS y guardarlo en la BD. 
import json
import requests
import os
import random
import time


# Documentación de investigación Django IP's: https://docs.djangoproject.com/es/5.1/ref/validators/
"""Dato Random: Al principio perdí mucho tiempo usando diversos, headers y proxies para intentar bypassear el trafico,
   pero la misma pagina me dice que cada 15 min puedo volver a obtener la lista así que no hay problema, cada 15 actualizo"""

# Ruta del archivo para almacenar la última actualización
LAST_UPDATE_FILE = 'last_update.txt'
IPS_FILE = 'ips-tor1.txt'


################################################################################## Métodos/Funciones ##################################################################################

############ GET

def fetch_tor_ips():
    url = 'https://www.dan.me.uk/torlist/?full'
    #url2 = 'https://www.bigdatacloud.com/'
    ips = set()
    try:
        response = requests.get(url, timeout=15) #un timeout de 15 si. 
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        ip_lines = soup.get_text().splitlines()
        for ip in ip_lines:
            if ip.strip():
                ips.add(ip.strip())
        time.sleep(10) #espero 10 segundos entre solicitudes.
    except requests.RequestException as e:
        print(f"Error fetching IPs from {url}: {e}")

    return list(ips)

def save_ips_to_file(ips, filename=IPS_FILE):
    try:
        with open(filename, 'w') as file:
            for ip in ips:
                file.write(f"{ip}\n")
        print(f"IPs saved to {filename}")
    except IOError as e:
        print(f"Error saving IPs to file: {e}")

def read_ips_from_file(filename=IPS_FILE):
    try:
        with open(filename, 'r') as file:
            ips = file.readlines()
        # Limpia las IPs de espacios en blanco y saltos de línea
        return [ip.strip() for ip in ips]
    except FileNotFoundError:
        return []  # Devuelve una lista vacía si el archivo no existe

def update_last_update_time():
    with open(LAST_UPDATE_FILE, 'w') as file:
        file.write(str(time.time()))

def get_last_update_time():
    if os.path.exists(LAST_UPDATE_FILE):
        with open(LAST_UPDATE_FILE, 'r') as file:
            return float(file.read().strip())
    return 0

############ POST

def exclude_tor_ips(request):
    try:
        data = json.loads(request.body)
        ip = data.get('ip')

        if not ip:
            return JsonResponse({'error': 'IP is required'}, status=400)
        
        # Validar IP
        try:
            validate_ipv4_address(ip)
        except ValidationError:
            try:
                validate_ipv6_address(ip)
            except ValidationError:
                return JsonResponse({'error': 'Invalid IP address'}, status=400)

        # Guardar en base de datos
        ExcludedIP.objects.get_or_create(ip_address=ip)

        # Guardar la IP en el archivo
        with open('ips-tor2.txt', 'a') as file:
            file.write(f"{ip}\n")

        return JsonResponse({'message': 'IP added successfully'}, status=200)
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON'}, status=400)


############ POST - FILTERED IP'S

def tor_ips_filtered():
    """Filtra las IPs de TOR excluyendo las IPs de la base de datos."""
    # Obtener IPs desde las fuentes externas
    all_ips = read_ips_from_file() #llamo a la def que almaceno las ips en el .txt, leo directamente el .txt
    
    # Obtener IPs excluidas de la base de datos
    excluded_ips = ExcludedIP.objects.values_list('ip_address', flat=True)
    excluded_ips_set = set(excluded_ips)
    #print(f'IPS EXCLUIDAS: {excluded_ips_set}')


    # Convertir todas las IPs de all_ips a conjunto para que sea compatible con excluded_ips_set
    all_ips_set = set(all_ips)
    #print(f'IPS SET: {all_ips_set}')

    # Filtrar IPs excluidas
    filtered_ips = all_ips_set - excluded_ips_set
    #print(f'IPS FILTRADAS: {filtered_ips}')

    
    return list(filtered_ips)

################################################################################## VISTAS ##################################################################################

# Primer vista para el Endpoint #1
@csrf_exempt
def tor_ips_view(request):
    current_time = time.time()
    last_update_time = get_last_update_time()

    # Actualiza las IPs si han pasado más de 15 minutos
    if current_time - last_update_time > 15 * 60:
        ips = fetch_tor_ips()
        save_ips_to_file(ips, filename=IPS_FILE)
        update_last_update_time()
    
    # Lee las IPs del archivo y devuelve la respuesta JSON
    ips_from_file = read_ips_from_file(filename=IPS_FILE)
    return JsonResponse({'ips': ips_from_file})

# Segunda vista para el Endpoint #2  
@require_http_methods(["POST"])  
@csrf_exempt
def exclude_ip_view(request):
    try:
        data = json.loads(request.body)
        response = exclude_tor_ips(request)
        return response
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

# Tercera vista para el Endpoint #3 - IP's Filtradas: Retornando todas las ips excepto las que se enviaron a la BD.    
#@require_GET
@require_http_methods(["GET"])  
def tor_ips_filtered_view(request):
    try:
        # Obtener las IPs filtradas
        filtered_ips = tor_ips_filtered()
        
        # Devolver las IPs en formato JSON
        return JsonResponse(filtered_ips, safe=False)
    except Exception as e: 
        return JsonResponse({'error': str(e)}, status=500)