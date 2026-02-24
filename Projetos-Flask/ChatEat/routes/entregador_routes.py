from flask import Blueprint
from routes.auth import admin_required, entregador_required
from controllers import entregador_controller

entregador_route = Blueprint('entregador', __name__)


@entregador_route.route('/painel_entregador')
@entregador_required
def painel_entregador():
    return entregador_controller.painel_entregador()


@entregador_route.route('/admin_entregador')
@admin_required
def admin_entregador():
    return entregador_controller.admin_entregador()


@entregador_route.route('/admin_entregador/adicionar',methods=['GET', 'POST'])
@admin_required
def admin_add_entregador():
    return entregador_controller.admin_add_entregador()


@entregador_route.route('/admin_entregador/visualizar')
@admin_required
def admin_view_entregador():
    return entregador_controller.admin_view_entregador()


@entregador_route.route('/admin_entregador/remover',methods=['POST', 'GET'])
@admin_required
def admin_remove_entregador():
    return entregador_controller.admin_remove_entregador()
