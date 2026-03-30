from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from chat.models import ChatMessage, ChatRoom
from models.auth_model import FriendshipRequest, User


class UserController:
    @staticmethod
    @login_required
    def profile(request, user_id):
        profile = get_object_or_404(User, id=user_id)
        current_user_id = request.user.id
        current_user = None
        if current_user_id:
            current_user = User.objects.filter(id=current_user_id).first()
        if request.method == 'POST' and current_user_id == profile.id:
            nome = request.POST.get('nome', '').strip()
            bio = request.POST.get('bio', '').strip()
            descricao = request.POST.get('descricao', '').strip()
            img = request.FILES.get('img')
            if nome:
                profile.nome = nome
            profile.bio = bio
            profile.descricao = descricao
            if img:
                profile.img = img
            profile.save()
            if img:
                request.session['user_img'] = profile.img.url
            return redirect('user_profile', user_id=profile.id)
        is_friend = False
        outgoing_request = None
        incoming_request = None
        if current_user and current_user_id != profile.id:
            is_friend = profile.friends.filter(id=current_user_id).exists()
            outgoing_request = FriendshipRequest.objects.filter(
                sender=current_user,
                receiver=profile,
                status=FriendshipRequest.STATUS_PENDING,
            ).first()
            incoming_request = FriendshipRequest.objects.filter(
                sender=profile,
                receiver=current_user,
                status=FriendshipRequest.STATUS_PENDING,
            ).first()

        return render(
            request,
            'user.html',
            {
                'profile': profile,
                'current_user_id': current_user_id,
                'is_friend': is_friend,
                'outgoing_request': outgoing_request,
                'incoming_request': incoming_request,
            },
        )

    @staticmethod
    @login_required
    def send_friend_request(request, user_id):
        if request.method != 'POST':
            return redirect('user_profile', user_id=user_id)

        current_user_id = request.user.id
        if current_user_id == user_id:
            return redirect('user_profile', user_id=user_id)

        sender = get_object_or_404(User, id=current_user_id)
        receiver = get_object_or_404(User, id=user_id)

        if receiver.friends.filter(id=sender.id).exists():
            return redirect('user_profile', user_id=user_id)

        reverse_pending = FriendshipRequest.objects.filter(
            sender=receiver,
            receiver=sender,
            status=FriendshipRequest.STATUS_PENDING,
        ).first()
        if reverse_pending:
            return redirect('user_profile', user_id=user_id)

        existing_request = FriendshipRequest.objects.filter(
            sender=sender,
            receiver=receiver,
        ).first()

        if existing_request:
            if existing_request.status == FriendshipRequest.STATUS_DECLINED:
                existing_request.status = FriendshipRequest.STATUS_PENDING
                existing_request.save(update_fields=['status'])
            return redirect('user_profile', user_id=user_id)

        FriendshipRequest.objects.create(
            sender=sender,
            receiver=receiver,
            status=FriendshipRequest.STATUS_PENDING,
        )

        return redirect('user_profile', user_id=user_id)

    @staticmethod
    @login_required
    def accept_friend_request(request, request_id):
        if request.method != 'POST':
            return redirect('home')

        current_user_id = request.user.id
        friend_request = get_object_or_404(
            FriendshipRequest,
            id=request_id,
            receiver_id=current_user_id,
        )

        if friend_request.status != FriendshipRequest.STATUS_PENDING:
            return redirect('user_profile', user_id=friend_request.sender.id)

        friend_request.status = FriendshipRequest.STATUS_ACCEPTED
        friend_request.save(update_fields=['status'])
        friend_request.sender.friends.add(friend_request.receiver)
        friend_request.receiver.friends.add(friend_request.sender)

        return redirect('user_profile', user_id=friend_request.sender.id)

    @staticmethod
    @login_required
    def decline_friend_request(request, request_id):
        if request.method != 'POST':
            return redirect('home')

        current_user_id = request.user.id
        friend_request = get_object_or_404(
            FriendshipRequest,
            id=request_id,
            receiver_id=current_user_id,
        )

        if friend_request.status != FriendshipRequest.STATUS_PENDING:
            return redirect('user_profile', user_id=friend_request.sender.id)

        friend_request.status = FriendshipRequest.STATUS_DECLINED
        friend_request.save(update_fields=['status'])

        return redirect('user_profile', user_id=friend_request.sender.id)

    @staticmethod
    @login_required
    def friends_list(request):
        current_user_id = request.user.id
        current_user = (
            User.objects.prefetch_related('friends')
            .filter(id=current_user_id)
            .first()
        )
        friends = []
        friends_with_unread = []
        if current_user:
            friends = current_user.friends.all().order_by('nome')
            for friend in friends:
                room_name = f'friend_{min(current_user.id, friend.id)}_{max(current_user.id, friend.id)}'
                room = ChatRoom.objects.filter(name=room_name).first()
                if not room:
                    friends_with_unread.append({'friend': friend, 'unread': 0})
                    continue
                unread_count = (
                    ChatMessage.objects.filter(room=room, sender=friend)
                    .exclude(read_by=current_user)
                    .count()
                )
                friends_with_unread.append({'friend': friend, 'unread': unread_count})

        return render(
            request,
            'friends.html',
            {
                'friends': friends,
                'friends_with_unread': friends_with_unread,
            },
        )
