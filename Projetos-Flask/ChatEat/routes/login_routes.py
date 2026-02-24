from flask import Blueprint
from routes.auth import login_required
from controllers import login_controller

login_route = Blueprint('Login',__name__)

@login_route.route('/login')
def login():
    return login_controller.login()

@login_route.route('/recuperar-senha', methods=['GET', 'POST'])
def recuperar_senha():
    return login_controller.recuperar_senha()

@login_route.route('/cadastro')
def cadastro():
    return login_controller.cadastro()

@login_route.route('/cadastro_cliente', methods=['POST'])
def inserir():
    return login_controller.inserir()

@login_route.route('/busca', methods=['POST'])
def busca():
    return login_controller.busca()

@login_route.route('/logout')
@login_required
def logout():
    return login_controller.logout()
