from django.db import models
from django.utils import timezone

# Create your models here.

# Este será el modelo para almacenar todas las direcciones IPS que obtengamos. 
class All_ips(models.Model):
    ip_address = models.GenericIPAddressField(unique=True)
    created_at = models.DateTimeField(auto_now_add=True) #Esto lo omitiré por el momento, realmente necesito primero comprobar las ips

    def __str__(self):
        return self.ip_address

class ExcludedIP(models.Model):
    ip_address = models.GenericIPAddressField(unique=True)
    created_at = models.DateTimeField(default=timezone.now, blank=True)

    def __str__(self):
        return self.ip_address