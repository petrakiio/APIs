from django.shortcuts import get_object_or_404, render
from models.auth_model import User


class UserController:
    @staticmethod
    def profile(request, user_id):
        profile = get_object_or_404(User, id=user_id)
        return render(request, 'user.html', {'profile': profile})
