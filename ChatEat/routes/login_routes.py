from flask import Blueprint,flash,render_template,url_for,request,redirect,session
import os
from routes.auth import login_required
from class_profile.login_class import Pessoa,PersonaService

login_route = Blueprint('Login',__name__)

@login_route.route('/login')
def login():
    return render_template('login.html')

@login_route.route('/cadastro')
def cadastro():
    return render_template('cadastro.html')

@login_route.route('/cadastro_cliente', methods=['POST'])
def inserir():
    pessoa = Pessoa(
        nome=request.form.get('usuario'),
        senha=request.form.get('senha'),
        email=request.form.get('email'),
        data=request.form.get('data'),
    )

    resultado = PersonaService.cadastrar(pessoa)

    if resultado['ok']:
        flash('Cadastro realizado com sucesso! Faça seu login.', 'success')
        return redirect(url_for('Login.login'))

    flash(resultado['msg'], 'danger')
    return redirect(url_for('Login.cadastro'))

@login_route.route('/busca', methods=['POST'])
def busca():
    pessoa = Pessoa(
        nome=request.form.get('usuario'),
        senha=request.form.get('senha'),
        email=None,
        data=None
    )

    resultado = PersonaService.login(pessoa)

    if not resultado['ok']:
        flash(resultado['msg'], 'danger')
        return redirect(url_for('Login.login'))

    cliente = resultado['cliente']

    session['usuario_id'] = cliente['id']
    session['usuario_nome'] = cliente['usuario']
    session['usuario_image'] = cliente['foto_perfil']
    session['is_admin'] = bool(cliente['is_admin'])
    session.permanent = True

    flash('Login realizado com sucesso!', 'success')
    return redirect(url_for('home.index'))

@login_route.route('/logout')
@login_required
def logout():
    session.pop('usuario_id', None)
    session.pop('usuario_nome', None)
    session.pop('usuario_image', None)  
    session.clear()
    return redirect(url_for('home.index'))
