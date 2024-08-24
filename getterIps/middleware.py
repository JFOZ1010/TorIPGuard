import logging
import time
import datetime
import logging

#logger = logging.getLogger('django')
logger = logging.getLogger('getterIps.middleware')



# Clase de middleware para la request que se hagan, toma la peticion, la respuesta de la peticion, y la duracion. 
class RequestLoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    # maneja la solicitud y respuesta, y pues registra el método HTTP, con lo que devuelve de la linea 18 a la 20
    def __call__(self, request):
        start_time = time.time()
        response = self.get_response(request)
        duration = time.time() - start_time

        logger.info(
            f"Request: {request.method} {request.get_full_path()} "
            f"Response Status: {response.status_code} "
            f"Duration: {duration:.2f}s"
        )
        return response
    
class DeviceBrowserLoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        user_agent = request.META.get('HTTP_USER_AGENT', 'Unknown')

        # Registrar la información obtenida
        logger.debug(
            f"User-Agent: {user_agent}"
        )

        # Llamar al siguiente middleware o vista
        response = self.get_response(request)
        return response

    
#Esta clase rregistra el identificador del usuario autenticado y la URL a la que accede. 
class UserAuditingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Captura el identificador del usuario autenticado si existe
        user = request.user
        user_id = getattr(user, 'id', 'Anonymous')  # 'Anonymous' si el usuario no está autenticado
        
        # Log de auditoría antes de procesar la solicitud
        if user_id != 'Anonymous':
            logger.info(f"ID Usuario: {user_id} hizó una petición a: {request.path}")

        # Procesa la solicitud
        response = self.get_response(request)

        # Log de auditoría después de procesar la solicitud (opcional)
        if user_id != 'Anonymous':
            logger.info(f"ID Usuario: {user_id} recibió un estado de respuesta: {response.status_code}")

        return response

# Esta clase de middleware solo sera como pa mostear la hora y fecha, en caso de que necesite uno revisar algo en especifio de tal fecha.
class RequestTimeLoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Obtener la fecha y hora actual en formato legible
        current_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        # Registrar la fecha y hora junto con la ruta solicitada
        logger.debug(f"Hora de petición: {current_time} | Endpoint: {request.get_full_path()}")

        # Llamar al siguiente middleware o vista
        response = self.get_response(request)
        return response