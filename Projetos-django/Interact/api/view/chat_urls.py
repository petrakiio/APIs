from django.urls import path

from controller.chat.chat_controller import ChatController

urlpatterns = [
    path('chat/<int:room_id>/', ChatController.room, name='chat-room'),
]
