from django.contrib.auth import get_user_model
from django.shortcuts import render

class HomeController:
    @staticmethod
    def index(request):
        User = get_user_model()
        current_user = None

        if request.user.is_authenticated:
            current_user = request.user
            users = User.objects.exclude(id=request.user.id).order_by('id')
        else:
            user_id = request.session.get('user_id')
            if user_id:
                current_user = User.objects.filter(id=user_id).first()
                users = User.objects.exclude(id=user_id).order_by('id')
            else:
                users = User.objects.all().order_by('id')

        return render(request, 'index.html', {'users': users, 'current_user': current_user})
