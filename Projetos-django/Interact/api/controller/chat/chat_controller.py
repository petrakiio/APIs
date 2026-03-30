from django.http import HttpResponseForbidden
from django.shortcuts import render

from chat.models import ChatMessage, ChatRoom
from models.auth_model import User


class ChatController:
    @staticmethod
    def room(request, user_id):
        current_user = request.user if request.user.is_authenticated else None
        if not current_user:
            return HttpResponseForbidden('Login necessario para acessar o chat.')

        friend = User.objects.filter(id=user_id).first()
        if not friend:
            return HttpResponseForbidden('Usuario nao encontrado.')

        are_friends = current_user.friends.filter(id=friend.id).exists()

        if not are_friends:
            return HttpResponseForbidden('Voce so pode conversar com amigos.')

        room_name = f'friend_{min(current_user.id, friend.id)}_{max(current_user.id, friend.id)}'
        room, _ = ChatRoom.objects.get_or_create(name=room_name, defaults={'name': room_name})
        room.participants.add(current_user, friend)
        messages = ChatMessage.objects.filter(room=room).select_related('sender')
        unread_ids = list(
            messages.exclude(read_by=current_user)
            .values_list('id', flat=True)
        )
        if unread_ids:
            through = ChatMessage.read_by.through
            through.objects.bulk_create(
                [
                    through(chatmessage_id=message_id, user_id=current_user.id)
                    for message_id in unread_ids
                ],
                ignore_conflicts=True,
            )

        return render(
            request,
            'chat.html',
            {
                'room': room,
                'messages': messages,
                'current_user': current_user,
                'friend': friend,
            },
        )
