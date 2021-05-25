from django.http import request
from django.shortcuts import render

def index(request):
    return render(request, 'chat/index.html')

def room(request, room_name):
    return render(request, 'chat/room.html', {
        'room_name': room_name
    })

#Vistas para los templates de abrir y administrar coneccion
def abrir_conexion(request):
    return render(request,'abrirConexion.html')

def administrar_conexion(request):
    conexiones =['Nombre usuario','example@gmail.com',123456789]
    return render(request, 'administrarConexion.html',{'conexiones':conexiones})

# Create your views here.
