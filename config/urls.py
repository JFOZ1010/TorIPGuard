"""config URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.http import HttpResponse
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView


def home_view(request):
    html = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>API REST GetterIPS</title>
    <!-- Bootstrap CSS -->
    <link href="https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css" rel="stylesheet">
    <!-- JetBrains Mono Font -->
    <link href="https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;700&display=swap" rel="stylesheet">
    <style>
        html, body {
            height: 100%;
            margin: 0;
            padding: 0;
        }
        body {
            background-color: #f8f9fa;
            display: flex;
            flex-direction: column;
            font-family: 'JetBrains Mono', monospace;
        }
        .hero-section {
            background-color: #343a40;
            color: #ffffff;
            padding: 60px 0;
        }
        .hero-section h1 {
            font-size: 3rem;
            margin-bottom: 20px;
        }
        .hero-section p {
            font-size: 1.25rem;
        }
        .container {
            flex: 1;
            margin-top: 30px;
            margin-bottom: 20px; /* Ajustado para espacio antes del footer */
        }
        .list-group-item {
            margin-bottom: 10px; /* Añade espacio entre elementos de la lista */
            font-family: 'JetBrains Mono', monospace;
        }
        .footer {
            background-color: #343a40;
            color: #ffffff;
            padding: 20px 0;
            text-align: center;
            width: 100%;
            margin-top: auto; /* Asegura que el pie de página esté en la parte inferior */
        }
        .endpoints-section {
            margin-bottom: 40px; /* Ajustado para menor espacio arriba del footer */
        }
    </style>
</head>
<body>
    <div class="hero-section text-center">
        <div class="container">
            <h1>Bienvenido a la API de Gestión de IPs</h1>
            <p>Esta API te permite gestionar IPs maliciosas de redes TOR.</p>
        </div>
    </div>
    
    <div class="container">
        <h2 class="mt-5">Endpoints Públicos</h2>
        <ul class="list-group">
            <li class="list-group-item"><a href="/admin/">Panel de administración</a></li>
            <li class="list-group-item"><a href="/docs/">Documentación de la API (Swagger)</a></li>
            <li class="list-group-item"><a href="/redocs/">Otra vista de la documentación (Redoc)</a></li>
        </ul>
        
        <h2 class="mt-5">Endpoints de Autenticación</h2>
        <ul class="list-group">
            <li class="list-group-item"><a href="/auth/token/">Generar token JWT</a></li>
            <li class="list-group-item"><a href="/auth/token/refresh/">Refrescar token JWT</a></li>
            <li class="list-group-item"><a href="/auth/token/verify/">Verificar token JWT</a></li>
        </ul>
        
        <h2 class="mt-5 mb-4 endpoints-section">Endpoints de Gestión de IPs</h2>
        <ul class="list-group">
            <li class="list-group-item"><a href="/getterIPS/">Acceder a los endpoints de `getterIPS/` (requiere autenticación)</a></li>
        </ul>
    </div>
    
    <div class="footer">
        <p>Desarrollador: <a href="https://github.com/JFOZ1010" class="text-white" target="_blank">Juan Felipe Osorio</a></p>
    </div>
    
    <!-- Bootstrap JS -->
    <script src="https://code.jquery.com/jquery-3.5.1.slim.min.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/@popperjs/core@2.5.3/dist/umd/popper.min.js"></script>
    <script src="https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/js/bootstrap.min.js"></script>
</body>
</html>
    """
    return HttpResponse(html)


schema_view = get_schema_view(
    openapi.Info(
        title="Reto BISO - Documentation :-)",
        default_version='v1',
        description="Esta es la documentación del reto para la vacante BISO - Mercado Libre.",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="juanfelipeoz.rar@gmail.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('', home_view, name='home'),  # Define el home en la raíz del proyecto
    path('admin/', admin.site.urls),

    path('auth/', include([
        path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
        path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
        path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    ])),

    # Incluye las URLs de mi app `getterIps`
    path('getterIPS/', include('getterIps.urls')),
    path('docs/', schema_view.with_ui('swagger',
         cache_timeout=0), name='schema-swagger-ui'),
    path('redocs/', schema_view.with_ui('redoc',
         cache_timeout=0), name='schema-redoc'),
]
