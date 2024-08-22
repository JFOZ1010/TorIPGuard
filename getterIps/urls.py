from django.urls import path
from . import views

urlpatterns = [
    path('tor-ips/', views.tor_ips_view, name='tor_ips'), #esto despues lo debería modificar a endpoint1 GET, endpoint2 POST, endpoint3 GET
]