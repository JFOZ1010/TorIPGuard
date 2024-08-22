from django.urls import path
from . import views

urlpatterns = [
    path('tor-ips/', views.tor_ips_view, name='tor_ips'), #esto despues lo debería modificar a endpoint1 GET, endpoint2 POST, endpoint3 GET
    path('excluded-ips/', views.exclude_ip_view, name='excluded_ips'),
    path('filtered-ips/', views.tor_ips_filtered_view, name='filtered_ips')
]