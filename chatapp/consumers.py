# chat/consumers.py
import json
from channels.generic.websocket import AsyncWebsocketConsumer
from .models import  *
from django.contrib.auth import get_user_model

User = get_user_model()

class ChatConsumer(AsyncWebsocketConsumer):
    #definimos una metodo para burcar el mensage en la bse de datos
    def buscar_mensages(self, data):
        mensages = Mensaje.ultimos_10_mensajes()
        content = {
            'mensages': self.mensages_to_json(mensages)
        }
        self.enviar_chat_mensage(content)
        pass

    #defimos una metodo para un nuevo mensage
    def nuevo_mensage(self, data):
        emisor = data['from']
        emisor_usuario = User.objects.filter(username=emisor)[0]
        mensage = Mensaje.objects.create(emisor = emisor_usuario, contenido = data['mensage'])
        content = {
            'command':'nuevo_mensage',
            'mensage':self.mensage_to_json(mensage)
        }
        return self.enviar_chat_mensage(content)
    
    def mensages_to_json(self, mensages):
        resultado = []
        for mensage in mensages:
            resultado.append(self.mensage_to_json(mensage))
        return resultado

    def mensage_to_json(self, mensage):
        return {
            'emisor': mensage.emisor.username,
            'contenido': mensage.contenido,
            'fecha_hora': str(mensage.fecha_hora),
        }
    
    commands = {
        'buscar_mensages' : buscar_mensages,
        'nuevo_mensage':nuevo_mensage,
    }

    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name

        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    async def receive(self, text_data):
        data = json.loads(text_data)
        self.commands[data['command']](self, data)


    async def enviar_chat_mensage(self, message):
        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message
            }
        )

    # Receive message from room group
    def enviar_mensage(self, message):
        self.text_data=json.dumps(message)

    async def chat_message(self, event):
        message = event['message']

        # Send message to WebSocket
        await self.send(text_data=json.dumps(message))