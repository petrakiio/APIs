from django.shortcuts import render


class LoginController:
    @staticmethod
    def login(request):
        return render(request, 'login.html')

    @staticmethod
    def signup(request):
        return render(request, 'cadastro.html')
