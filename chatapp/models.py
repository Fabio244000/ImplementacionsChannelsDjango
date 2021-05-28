from django.db import models
from django.db.models.base import Model
from django.db.models.deletion import CASCADE, PROTECT
from django.contrib import admin
from django.db.models.fields import CharField

#Estamos declarando los modelos Operador, Cliente, Salachat y Mensaje
class Operdador(models.Model):
    nombre = models.CharField(max_length=50)
    correo = models.EmailField(max_length=50)
    celular = models.CharField(max_length=9)

    def __str__(self): 
        return self.nombre

class Cliente(models.Model):
    nombre = models.CharField(max_length=50)
    correo = models.EmailField(max_length=70)
    celular = models.CharField(max_length=9)

    def __str__(self): 
        return self.nombre

class Salachat(models.Model):
    nombre = models.CharField(max_length=100)
    apertura = models.DateTimeField()
    estado = models.BooleanField()
    cierre = models.DateTimeField()
    operador = models.ForeignKey(Operdador, on_delete=PROTECT)
    cliente = models.OneToOneField(Cliente, on_delete=CASCADE)

    def __str__(self) :
        return '%s %s' % (self.nombre, self.estado)

class Mensaje(models.Model):
    contenido = models.TextField(max_length=300)
    emisor = models.CharField(max_length=50)
    fecha_hora = models.DateTimeField()
    sala = models.ForeignKey(Salachat, on_delete=CASCADE)

    def __str__(self) :
        return '%s %s' % (self.emisor, self.contenido)
