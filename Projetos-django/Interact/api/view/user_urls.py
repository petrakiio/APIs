from django.urls import path
from controller.user.user_controller import UserController

urlpatterns = [
    path('user/<int:user_id>/', UserController.profile, name='user_profile'),
]
