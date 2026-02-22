from flask import Blueprint
from routes.auth import login_required
from controllers import profile_controller

profile_route = Blueprint('profile', __name__)

@profile_route.route('/perfil')
@login_required
def perfil():
    return profile_controller.perfil()

@profile_route.route('/upload-image', methods=['POST'])
@login_required
def atualizar_imagem():
    return profile_controller.atualizar_imagem()


@profile_route.route('/deletar/<int:usuario_id>', methods=['POST'])
@login_required
def deletar_conta(usuario_id):
    return profile_controller.deletar_conta(usuario_id)
