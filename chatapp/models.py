from django.db import models
from django.db.models.base import Model
from django.db.models.deletion import CASCADE, PROTECT
from django.contrib import admin
from django.db.models.fields import CharField
from django.contrib.auth import get_user_model

User = get_user_model()

#Estamos declarando los modelos Operador, Cliente, Salachatn usuario, estamos normalizando 
class Usuario(models.Model):
    nombre_usuario = models.CharField(max_length = 50)
    clave_usuario = models.CharField(max_length = 50)
    correo = models.EmailField()
    celular = models.IntegerField()
    status = models.BooleanField()
    tipo = models.CharField(max_length=30)#para saber si esta logueado o no, tiene valor False si esta desconectado y True si esta conectado en el isietam

    def __str__(self) -> str:
        return '%s %s' %(self.nombre_usuario, self.tipo)


class Empleado(models.Model):
    id_usuario = models.OneToOneField(Usuario, on_delete=PROTECT)
    nombre_empleado = models.CharField(max_length=70)
    apellidos_empleado = models.CharField(max_length=70)
    tipo_empleado = models.CharField(max_length=50)

    def __str__(self): 
        return self.nombre_empleado

class Cliente(models.Model):
    id_usuario = models.OneToOneField(Usuario, on_delete=CASCADE)
    nombre_cliente = models.CharField(max_length=70)
    apellidos_cliente = models.CharField(max_length=70)
    #otros atributos propios de los clientes

    def __str__(self): 
        return self.nombre_cliente

class Salachat(models.Model):
    nombre = models.CharField(max_length=100)
    apertura = models.DateTimeField()
    estado = models.BooleanField()
    cierre = models.DateTimeField()
    operador = models.ForeignKey(Empleado, on_delete=PROTECT)
    cliente = models.OneToOneField(Cliente, on_delete=CASCADE)

    def __str__(self) :
        return '%s %s' % (self.nombre, self.estado)



class Mensaje(models.Model):
    contenido = models.TextField(max_length=300)#base de datos no relacional
    emisor = models.ForeignKey(User, related_name='autor_mensage', on_delete=CASCADE)
    fecha_hora = models.DateTimeField()
    sala = models.ForeignKey(Salachat, on_delete=CASCADE)
    #crear una clase intermedia

    def __str__(self) :
        return self.emisor.username

    def ultimos_10_mensajes(self):
        return Mensaje.objects.order_by('-').all('-fecha_hora')[:10]


