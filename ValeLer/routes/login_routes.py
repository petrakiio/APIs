from flask import Blueprint
from routes.auth import login_required
from controllers import login_controller

login = Blueprint('Login', __name__)


@login.route('/login', methods=['GET', 'POST'])
def login_page():
    return login_controller.login_page()


@login.route('/cadastro', methods=['GET', 'POST'])
def cadastro_page():
    return login_controller.cadastro_page()


@login.route('/logout')
@login_required
def logout():
    return login_controller.logout()
