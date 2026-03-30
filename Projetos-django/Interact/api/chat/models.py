from django.db import models
from models.auth_model import User


class ChatRoom(models.Model):
    name = models.CharField(max_length=120, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    participants = models.ManyToManyField(User, related_name='chat_rooms')

    def __str__(self):
        return self.name


class ChatMessage(models.Model):
    TYPE_TEXT = 'text'
    TYPE_IMAGE = 'image'
    TYPE_AUDIO = 'audio'

    TYPE_CHOICES = [
        (TYPE_TEXT, 'Texto'),
        (TYPE_IMAGE, 'Imagem'),
        (TYPE_AUDIO, 'Audio'),
    ]

    room = models.ForeignKey(ChatRoom, on_delete=models.CASCADE, related_name='messages')
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='chat_messages')
    message_type = models.CharField(max_length=10, choices=TYPE_CHOICES, default=TYPE_TEXT)
    text = models.TextField(blank=True)
    file = models.FileField(upload_to='chat/', blank=True, null=True)
    read_by = models.ManyToManyField(User, related_name='read_messages', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        return f'{self.sender} - {self.message_type}'
