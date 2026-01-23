import json
import os
import google.generativeai as genai
from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import sync_to_async

genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))
model = genai.GenerativeModel('gemini-3-flash-preview')

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

        respuesta_ia = await sync_to_async(self.obtener_respuesta_gemini)(mensaje_usuario)

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': respuesta_ia
            }
        )

    def obtener_respuesta_gemini(self, consulta):
        try:
            response = model.generate_content(consulta)
            return response.text
        except Exception as e:
            return f"Hubo un problema al contactar a la IA: {str(e)}"

    async def chat_message(self, event):
        message = event['message']
        await self.send(text_data=json.dumps({
            'message': message
        }))