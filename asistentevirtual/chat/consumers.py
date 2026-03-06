import json
from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import sync_to_async
from .gemini_utils import obtener_respuesta_gemini 
from .models import AsistenteConfig


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_group_name = "chat_asistente_room"
        
        await self.channel_layer.group_add(
            self.room_group_name, 
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        mensaje_usuario = text_data_json['message']

        personalidad = await self.get_personalidad()

        respuesta_ia = await sync_to_async(self.obtener_respuesta_gemini)(mensaje_usuario, personalidad)

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': respuesta_ia
            }
        )

    @sync_to_async
    def get_personalidad(self):
        config = AsistenteConfig.objects.filter(user=self.scope["user"]).first()
        if config:
            return config.personalidad
        return "Eres un asistente servicial."

    async def chat_message(self, event):
        message = event['message']
        await self.send(text_data=json.dumps({
            'message': message
        }))