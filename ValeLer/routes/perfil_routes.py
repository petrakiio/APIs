from flask import Blueprint
from routes.auth import login_required
from controllers import perfil_controller

perfil = Blueprint('Perfil', __name__)


@perfil.route('/perfil', methods=['GET', 'POST'])
@login_required
def perfil_page():
    return perfil_controller.perfil_page()


@perfil.route('/devolver_emprestimo', methods=['POST'])
@login_required
def devolver_emprestimo():
    return perfil_controller.devolver_emprestimo()


@perfil.route('/atualizar_foto', methods=['POST'])
@login_required
def atualizar_foto():
    return perfil_controller.atualizar_foto()
