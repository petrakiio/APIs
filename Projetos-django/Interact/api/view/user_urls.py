from django.urls import path
from controller.user.user_controller import UserController

urlpatterns = [
    path('user/<int:user_id>/', UserController.profile, name='user_profile'),
    path('friends/', UserController.friends_list, name='friends_list'),
    path(
        'user/<int:user_id>/friend-request/',
        UserController.send_friend_request,
        name='friend_request_send',
    ),
    path(
        'friend-request/<int:request_id>/accept/',
        UserController.accept_friend_request,
        name='friend_request_accept',
    ),
    path(
        'friend-request/<int:request_id>/decline/',
        UserController.decline_friend_request,
        name='friend_request_decline',
    ),
]
