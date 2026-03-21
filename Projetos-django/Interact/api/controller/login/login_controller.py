from django.shortcuts import render


class LoginController:
    @staticmethod
    def login(request):
        return render(request, 'auth.html')

    @staticmethod
    def signup(request):
        return render(request, 'auth.html')
