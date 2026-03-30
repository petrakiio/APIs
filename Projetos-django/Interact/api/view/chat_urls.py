from django.urls import path

from controller.chat.chat_controller import ChatController

urlpatterns = [
    path('chat/user/<int:user_id>/', ChatController.room, name='chat-room'),
]
