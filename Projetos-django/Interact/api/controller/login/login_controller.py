from django.contrib import messages
from django.shortcuts import redirect, render
from models.auth_model import User

class LoginController:
    @staticmethod
    def login(request):
        if request.method == 'POST':
            email = request.POST.get('email','').strip()
            senha = request.POST.get('senha','').strip()
            remember = request.POST.get('remember_me') == 'on'
            if not email or not senha:
                messages.error(request,'Preencha email e senha')
                return redirect('login')
            result = User.login(email,senha)
            if result[0]:
                user = result[1]
                request.session['user_id'] = user.id
                request.session['user_nome'] = user.nome
                if remember:
                    request.session.set_expiry(60 * 60 * 24 * 30) #expira a sessão em 1 mês
                else:
                    request.session.set_expiry(0) #expira ao fechar o navegador
                return redirect('home')
            else:
                messages.error(request,result[1])
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

    @staticmethod
    def logout(request):
        request.session.flush()
        return redirect('login')
