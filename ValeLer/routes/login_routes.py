from flask import Blueprint, render_template, redirect, url_for, request, session
from models.login import Pessoa,PessoaService
from routes.auth import login_required
from models.tools.get_ip import get_ip
from models.tools.brute_force_guard import brute_force_guard

login = Blueprint('Login', __name__)


@login.route('/login', methods=['GET', 'POST'])
def login_page():
    if request.method == 'POST':
        gmail = request.form.get('gmail')
        senha = request.form.get('password')
        ip = get_ip()

        # Se já está em lockout por IP/conta, não processa nova tentativa.
        blocked, wait_seconds = brute_force_guard.check_block(ip, gmail)
        if blocked:
            return render_template(
                'login.html',
                error=(
                    f"Muitas tentativas. Tente novamente em {wait_seconds} segundos."
                ),
            )

        result = PessoaService.login(gmail, senha)
        if result[0]:
            # Login válido: limpa tentativas anteriores desta origem/conta.
            brute_force_guard.register_success(ip, gmail)
            session['usuario_id'] = result[2]['id_cliente']
            session['nome'] = result[2]['nome']
            session['gmail'] = result[2]['gmail']
            session['img'] = result[2]['img_user']
            session['is_admin'] = result[2]['is_admin']
            return redirect(url_for('Home.index'))
        else:
            # Login inválido: contabiliza para possível bloqueio.
            brute_force_guard.register_failure(ip, gmail)
            return render_template('login.html', error=result[1])
    return render_template('login.html')

@login.route('/cadastro', methods=['GET', 'POST'])
def cadastro_page():
    if request.method == 'POST':
        nome = request.form.get('nome')
        gmail = request.form.get('gmail')
        senha = request.form.get('password')
        is_admin = request.form.get('is_admin') == 'on'
        user = Pessoa(nome, gmail, senha, is_admin)
        result = PessoaService.cadastrar(user)
        if result[0]:
            return redirect(url_for('Login.login_page'))
        else:
            return render_template('cadastro.html', error=result[1])
    return render_template('cadastro.html')       


@login.route('/logout')
@login_required
def logout():
    session.clear()
    return redirect(url_for('Home.index'))
