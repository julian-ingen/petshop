from django.db import models

from django.contrib.auth.models import User

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(blank=True, null=True)
    birthday = models.DateField(blank=True, null=True)

    def __str__(self):
        return self.user.username

class Producto(models.Model):
    nombre = models.CharField(max_length=100,verbose_name='nombre')
    descripcion = models.CharField(max_length=100,verbose_name='descripcion')
    precio = models.IntegerField(verbose_name='precio')
    imagen_url = models.URLField(verbose_name="imagen_url")
    ean =models.BigIntegerField(verbose_name='ean', unique =True)
    empresa = models.CharField(max_length=100, verbose_name='Empresa', default='Desconocido')

    def __str__(self):
        return f"{self.nombre}| {self.descripcion}|${self.precio}" 

