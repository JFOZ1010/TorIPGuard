from django.urls import path
from . import views

urlpatterns = [
    path('get-tor-ips/', views.tor_ips_view, name='tor_ips'), #esto despues lo debería modificar a endpoint1 GET, endpoint2 POST, endpoint3 GET
    path('post-excluded-ips/', views.exclude_ip_view, name='excluded_ips'),
    path('get-filtered-ips/', views.tor_ips_filtered_view, name='filtered_ips'),
    path('count_excluded_ips/', views.count_excluded_ips_view, name='count_excluded_ips_view'),
    path('ip_stats/', views.ip_stats_view, name='ip_stats_view'),
    path('count-all-ips/', views.count_all_ips_view, name='count_ips_in_file'),
    path('update-excluded-ip/', views.update_excluded_ip_view, name='update_excluded_ip'),
    path('delete-excluded-ip/<str:ip_address>/', views.delete_specific_excluded_ip_view, name='delete_specific_excluded_ip'),    
    
    
    ## Dejo métodos adicionales para la API - Por el momento no funcionales.
    #path('get-ip-excluded/<str:ip_address>/', views.ip_excluded_details_view, name='get_ip_details'),
    #path('delete-ip-excluded/<str:ip_address>/', views.delete_ip_excluded_view, name='delete_ip'),
    #path('get-ips/excluded/', views.excluded_ips_list_view, name='excluded_ips_list'),
    #path('ips_by_date_range/', views.ips_by_date_range_view, name='ips_by_date_range_view'),

]