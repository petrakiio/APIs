from django.shortcuts import render
from models.auth_model import User

class HomeController:
    @staticmethod
    def index(request):
        current_user = None
        user_id = request.session.get('user_id')
        if user_id:
            current_user = User.objects.filter(id=user_id).first()
            users = User.objects.exclude(id=user_id).order_by('id')
        else:
            users = User.objects.all().order_by('id')

        return render(request, 'index.html', {'users': users, 'current_user': current_user})
