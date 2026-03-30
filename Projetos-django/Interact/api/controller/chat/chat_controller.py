from django.shortcuts import render

from chat.models import ChatMessage, ChatRoom


class ChatController:
    @staticmethod
    def room(request, room_id):
        current_user = request.user if request.user.is_authenticated else None
        room, _ = ChatRoom.objects.get_or_create(id=room_id, defaults={'name': f'Sala {room_id}'})
        messages = ChatMessage.objects.filter(room=room).select_related('sender')

        return render(
            request,
            'chat.html',
            {
                'room': room,
                'messages': messages,
                'current_user': current_user,
            },
        )
