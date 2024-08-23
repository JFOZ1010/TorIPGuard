from django.urls import path
from . import views

urlpatterns = [
    path('get-tor-ips/', views.tor_ips_view, name='tor_ips'), #esto despues lo debería modificar a endpoint1 GET, endpoint2 POST, endpoint3 GET
    path('post-excluded-ips/', views.exclude_ip_view, name='excluded_ips'),
    path('get-filtered-ips/', views.tor_ips_filtered_view, name='filtered_ips'),
    ## Dejo métodos adicionales para la API - Por el momento no funcionales.
    #path('get-ip-excluded/<str:ip_address>/', views.ip_excluded_details_view, name='get_ip_details'),
    #path('delete-ip-excluded/<str:ip_address>/', views.delete_ip_excluded_view, name='delete_ip'),
    #path('get-ips/excluded/', views.excluded_ips_list_view, name='excluded_ips_list'),

]