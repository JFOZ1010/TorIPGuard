from django.http import JsonResponse
import requests
import os
from bs4 import BeautifulSoup
from lxml import etree
import random
import time

"""Dato Random: Al principio perdí mucho tiempo usando diversos, headers y proxies para intentar bypassear el trafico,
   pero la misma pagina me dice que cada 15 min puedo volver a obtener la lista así que no hay problema, cada 15 actualizo"""

# Ruta del archivo para almacenar la última actualización
LAST_UPDATE_FILE = 'last_update.txt'
IPS_FILE = 'ips-tor1.txt'

def fetch_tor_ips():
    url = 'https://www.dan.me.uk/torlist/?full'
    #url2 = 'https://www.bigdatacloud.com/'
    ips = set()
    try:
        response = requests.get(url, timeout=15)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        ip_lines = soup.get_text().splitlines()
        for ip in ip_lines:
            if ip.strip():
                ips.add(ip.strip())
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