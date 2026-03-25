from django.shortcuts import render
from models.auth_model import User

class HomeController:
    @staticmethod
    def index(request):
        current_user = request.user if request.user.is_authenticated else None
        if current_user:
            users = User.objects.exclude(id=current_user.id).order_by('id')
        else:
            users = User.objects.all().order_by('id')

        return render(request, 'index.html', {'users': users, 'current_user': current_user})

    @staticmethod
    def search(request):
        codigo = request.POST.get('codigo', '').strip()
        current_user = request.user if request.user.is_authenticated else None
        if current_user:
            users = User.objects.exclude(id=current_user.id).order_by('id')
        else:
            users = User.objects.all().order_by('id')

        if codigo:
            users = users.filter(codigo_id=codigo)

        return render(request, 'index.html', {'users': users, 'current_user': current_user})
        
