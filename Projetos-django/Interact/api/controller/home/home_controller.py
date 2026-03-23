from django.shortcuts import render
from models.auth_model import User

class HomeController:
    @staticmethod
    def index(request):
        current_user = None
        user_id = request.session.get('user_id')
        if user_id:
            current_user = User.objects.filter(id=user_id).first()
        return render(request, 'index.html', {'current_user': current_user})
