# TorIPGuard

  

## Descripción del Proyecto

Este proyecto es una API REST para la gestión de IPs maliciosas en redes TOR. La API permite obtener, excluir, filtrar IPs, junto con otros endpoints, así como gestionar la autenticación y auditoría/logs de las solicitudes. Incluye un esquema de permisos que distingue entre usuarios normales y administradores.

**Prueba funcional `Endpoints` en video:** [Ver Video](https://drive.google.com/file/d/19Tovd27FzccF09oAFttbefHXdz0CWrja/view?usp=sharing)

**Demostración Entorno `venv` y `Docker`** 

<a href="https://asciinema.org/a/673511" target="_blank"><img src="https://asciinema.org/a/673511.svg" /></a>

## Solución Adicional

- **Solución Cloud GCP**: [Ver Documento](https://docs.google.com/document/d/1_MPDZHReXVXV71MRSsTcdpDIm9wBvWXF8lNe-VYk0bE/edit?usp=sharing)
  

## Tecnologías Implementadas

  

-  **Django**: Framework web para Python que se usa para desarrollar la API.

-  **Django REST Framework**: Extensión de Django para construir APIs RESTful.

-  **JWT (JSON Web Tokens)**: Para la autenticación de usuarios.

-  **Docker**: Para la contenerización de la aplicación.

-  **Docker Compose**: Para la orquestación de contenedores Docker.

- **PostgreSQL**: La base de datos relacional implementada para almacenar la información de Ip's Excluidas. 


## Requisitos

- Python 3.x

- Docker

- Docker Compose

  

## Instalación y Ejecución


1.  **Clona el repositorio**:

```bash
git clone https://github.com/JFOZ1010/Challenge-BISO.git

cd Challenge-BISO
```
 2. **Configura y corre la instancia de Docker**:
	 - Tener `Docker` y `Docker Compose` instalados.
	 - Corremos docker-compose:
	```bash
	-  docker-compose up --build
	```
3. **Accedemos a la API**: 
	 - La API estará disponible en `http://localhost:8000/`

## Uso de la API
### Endpoints Públicos
-   `GET /admin/` - Acceso al panel de administración de Django. No requiere autenticación.
-   `GET /docs/` - Documentación de la API. No requiere autenticación.
-   `GET /redocs/` - Otra vista de la documentación. No requiere autenticación.

### Endpoints de Autenticación
Para poder generar un token JWT, es necesario autenticarse como uno de los siguientes usuarios:

**Usuario Administrador**: 
	- *Nombre de usuario*: `useradmin` 
	- *Contraseña*: `adminadmin2001` 
	
**Usuario Normal**: 
	- *Nombre de usuario*: `usernormal` 
	- *Contraseña*: `useruser2001`

-   `POST /auth/token/` - Genera un token de autenticación JWT.
-   `POST /auth/token/refresh/` - Refresca el token JWT.
-   `POST /auth/token/verify/` - Verifica la validez de un token JWT.

### Endpoints bajo `getterIPS/`
#### Solo accesibles por el usuario Administrador

-   `POST /getterIPS/post-excluded-ips/` - Excluye una IP de la lista.
    
    -   **Formato de solicitud**: `{"ip": ""}`
-   `DELETE /getterIPS/delete-excluded-ip/<str:ip_address>/` - Elimina una IP excluida.
    
-   `PUT /getterIPS/update-excluded-ip/` - Actualiza una IP excluida.
    
    -   **Formato de solicitud**: `{"old_ip": "", "new_ip": ""}`
#### Accesibles por todos los usuarios autenticados

-   `GET /getterIPS/get-tor-ips/` - Obtiene todas las IPs de TOR.
-   `GET /getterIPS/get-filtered-ips/` - Obtiene todas las IPs excepto las excluidas.
-   `GET /getterIPS/count_excluded_ips/` - Cuenta las IPs excluidas.
-   `GET /getterIPS/ip_stats/` - Obtiene estadísticas de las IPs.
-   `GET /getterIPS/count-all-ips/` - Cuenta todas las IPs.

### Ejemplos de Solicitudes con `curl`
#### Obtener todas las IPs de TOR
	curl -X GET http://localhost:8000/getterIPS/get-tor-ips/ -H "Authorization: Bearer <token_jwt>"
#### Excluir una IP (Solo usuario administrador)
	curl -X POST http://localhost:8000/getterIPS/post-excluded-ips/ -H "Authorization: Bearer <token_jwt>" -H "Content-Type: application/json" -d '{"ip": "1.2.3.4"}'
#### Eliminar una IP excluida (Solo usuario administrador)
	curl -X DELETE http://localhost:8000/getterIPS/delete-excluded-ip/1.2.3.4/ -H "Authorization: Bearer <token_jwt>"
#### Actualizar una IP excluida (Solo usuario administrador)
	curl -X PUT http://localhost:8000/getterIPS/update-excluded-ip/ -H "Authorization: Bearer <token_jwt>" -H "Content-Type: application/json" -d '{"old_ip": "1.2.3.4", "new_ip": "5.6.7.8"}'
#### Obtener las IPs filtradas
	curl -X GET http://localhost:8000/getterIPS/get-filtered-ips/ -H "Authorization: Bearer <token_jwt>"
#### Contar las IPs excluidas
	curl -X GET http://localhost:8000/getterIPS/count_excluded_ips/ -H "Authorization: Bearer <token_jwt>"
 
### Licencia

1. **Propiedad**: Todos los derechos de propiedad intelectual sobre el código permanecen con Juan Felipe Osorio.

2. **Contacto**: Para cualquier consulta relacionada con el uso de este código, por favor contactarse conmigo a juanfelipeoz.rar@gmail.com

Muchas Gracias! 

Happy Hacking! :D
