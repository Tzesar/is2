from django.db import models

# Create your models here

class Usuario(models.Model):
    nombre_usuario = models.CharField(max_length=50)
    estado = models.IntegerField()
    password = models.CharField(max_length=128)
    nombres = models.CharField(max_length=50)
    apellidos = models.CharField(max_length=50)
    nro_telefono = models.CharField(max_length=13)
    email = models.CharField(max_length=128)
    observaciones = models.CharField(max_length=200)
