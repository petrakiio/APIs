from django.shortcuts import render
from django.http import HttpRequest
from models.auth_model import User

class LoginController:
    @staticmethod
    def login(request):
        if request.method == 'POST':
            pass
        return render(request, 'login.html')

    @staticmethod
    def signup(request):
        if request.method == 'POST':
            pass
        return render(request, 'cadastro.html')