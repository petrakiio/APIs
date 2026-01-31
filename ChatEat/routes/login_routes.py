from flask import Blueprint,flash,render_template,url_for,request,redirect
import os
from routes.auth import login_required
from class_profile.login_class import Pessoa,PersonaService

login_route = Blueprint('Login',__name__)

@login_route.route('/login')
@login_required
def login():
    return render_template('login.html')

@login_route.route('/cadastro')
@login_required
def cadastro():
    return render_template('cadastro.html')

@login_route.route('/cadastro_cliente', methods=['POST'])
def inserir():
    pessoa = Pessoa(
    usuario = request.form.get('usuario'),
    senha = request.form.get('senha'),
    email = request.form.get('email'),
    data = request.form.get('data'),
    )
    resultado = PersonaService(pessoa)
    if type(resultado) == bool:
        if resultado:
            flash('Cadastro realizado com sucesso! Faça seu login.','success')
            return redirect(url_for('Login.login'))
        else:
            flash('Erro ao realizar cadastro. Tente novamente.', 'danger')
            return redirect(url_for('Login.cadastro'))
    else:
        flash(resultado,'danger')
        return redirect(url_for('Login.cadastro'))
@login_route.route('/busca', methods=['POST', 'GET'])
def busca():
    if request.method == ['GET']:
        pass