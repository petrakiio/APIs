from django.contrib import messages
from django.shortcuts import redirect, render
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
            nome = request.POST.get('nome', '').strip()
            password = request.POST.get('password', '').strip()
            email = request.POST.get('email', '').strip()
            bio = request.POST.get('biografia', '').strip()
            descricao = request.POST.get('descricao', '').strip()
            if not nome or not password or not email:
                messages.error(request, 'Preencha nome, email e senha.')
                return redirect('signup')
            new_user = User(
                nome=nome,
                senha=User.criptografia(password),
                email=email,
                bio=bio,
                descricao=descricao,
                codigo_id = User.create_code(),
            )
            if new_user.Signup():
                messages.success(request,'Cadastro feito com sucesso')
                return redirect('home')
            else:
                messages.error(request,'Ouve um erro na inserção,por favor verifique seu Dados')
                return redirect('signup')

        return render(request, 'cadastro.html')
