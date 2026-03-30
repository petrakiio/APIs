import base64
import json

from asgiref.sync import sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer
from django.core.files.base import ContentFile
from django.utils import timezone

from chat.models import ChatMessage, ChatRoom


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_id = self.scope['url_route']['kwargs']['room_id']
        self.group_name = f'chat_{self.room_id}'

        user = self.scope.get('user')
        if not user or user.is_anonymous:
            await self.close()
            return

        await self._get_or_create_room()
        await self.channel_layer.group_add(self.group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.group_name, self.channel_name)

    async def receive(self, text_data=None, bytes_data=None):
        if not text_data:
            return

        payload = json.loads(text_data)
        message_type = payload.get('message_type', 'text')
        text = (payload.get('text') or '').strip()

        file_name = payload.get('file_name')
        file_data = payload.get('file_data')

        if message_type == ChatMessage.TYPE_TEXT and not text:
            return

        if message_type in (ChatMessage.TYPE_IMAGE, ChatMessage.TYPE_AUDIO):
            if not file_name or not file_data:
                return

        message = await self._create_message(
            message_type=message_type,
            text=text,
            file_name=file_name,
            file_data=file_data,
        )

        await self.channel_layer.group_send(
            self.group_name,
            {
                'type': 'chat.message',
                'payload': {
                    'id': message.id,
                    'room_id': self.room_id,
                    'sender': message.sender.nome,
                    'sender_id': message.sender.id,
                    'message_type': message.message_type,
                    'text': message.text,
                    'file_url': message.file.url if message.file else None,
                    'created_at': timezone.localtime(message.created_at).isoformat(),
                },
            },
        )

    async def chat_message(self, event):
        await self.send(text_data=json.dumps(event['payload']))

    @sync_to_async
    def _get_or_create_room(self):
        ChatRoom.objects.get_or_create(id=self.room_id, defaults={'name': f'Sala {self.room_id}'})

    @sync_to_async
    def _create_message(self, message_type, text='', file_name=None, file_data=None):
        room = ChatRoom.objects.get(id=self.room_id)
        user = self.scope['user']

        chat_message = ChatMessage(room=room, sender=user, message_type=message_type, text=text)

        if file_name and file_data:
            header, encoded = file_data.split(',', 1) if ',' in file_data else ('', file_data)
            try:
                decoded_file = base64.b64decode(encoded)
            except (ValueError, TypeError):
                decoded_file = b''
            chat_message.file.save(file_name, ContentFile(decoded_file), save=False)

        chat_message.save()
        return chat_message
